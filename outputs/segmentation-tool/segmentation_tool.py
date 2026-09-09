#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Segmentation Typing Tool Engine
===============================

Reads a DFA / multinomial "typing tool" workbook (.xlsm / .xlsx), works out its
structure by itself, and reproduces the classification chain:

    1. SUMPRODUCT(coefficients_for_segment, model_inputs)   -> DFA score
       (the `constant` row participates with an input of 1)
    2. EXP(score)                                           -> unnormalised weight
    3. weight / SUM(all weights) * 100                      -> probability %
    4. MATCH(MAX(probabilities), probabilities, 0)          -> winning position
    5. INDEX(segment_names, position)                       -> segment name

Nothing about the layout is hard-coded. The engine locates the SUMPRODUCT
formulas in the workbook and reads the column letters, row spans, recode rules
and segment names back out of them, so a 5-, 6-, 7- or n-segment model all work
from the same code path.

Author: generated for Ranjith.
"""

from __future__ import annotations

import argparse
import csv
import datetime as _dt
import math
import os
import re
import sys
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple

try:
    import openpyxl
    from openpyxl.utils import column_index_from_string, get_column_letter
except ImportError:  # pragma: no cover
    sys.stderr.write(
        "\nERROR: the 'openpyxl' package is missing.\n"
        "Install it with:  pip install openpyxl\n\n"
    )
    raise SystemExit(2)


# --------------------------------------------------------------------------
# Console helpers
# --------------------------------------------------------------------------

WARNINGS: List[str] = []


def warn(msg: str) -> None:
    WARNINGS.append(msg)
    print("  [WARN] " + msg)


def info(msg: str = "") -> None:
    print(msg)


def rule(title: str = "") -> None:
    if title:
        print("\n" + title)
        print("-" * max(len(title), 60))
    else:
        print("-" * 60)


# --------------------------------------------------------------------------
# BODMAS-correct arithmetic evaluator
# --------------------------------------------------------------------------
#
# Every number this tool produces goes through explicit, fully-parenthesised
# Python arithmetic, so precedence is never left to chance.  This evaluator
# exists for the *other* case: when a workbook contains a score/probability
# formula that is not one of the shapes we recognise, we still have to read its
# arithmetic correctly rather than guess.  It implements the standard
# precedence ladder:
#
#     B  brackets                    ( )
#     O  orders / exponent           ^
#     DM division & multiplication   / *          (left-associative, equal rank)
#     AS addition & subtraction      + -          (left-associative, equal rank)
#
# Two deliberate departures from textbook BODMAS, because the strings being
# parsed are Excel formulas and the answer has to be the one Excel gives:
#
#   1. Unary minus binds TIGHTER than the exponent, so -2^2 is 4, not -4.
#      Textbook convention says -4; Excel says 4.
#   2. The exponent is LEFT-associative, so 2^3^2 is (2^3)^2 = 64, not
#      2^(3^2) = 512.  Textbook convention says 512; Excel says 64.
#
# Both traps only bite on formulas that mix an exponent with a leading minus or
# with another exponent.  The scoring chain in these workbooks does neither, so
# the distinction never changes a segment - it is here so that a workbook
# variant using a different formula is still read the way Excel reads it.

_TOKEN_RE = re.compile(
    r"""
      (?P<num>\d+\.?\d*(?:[eE][+-]?\d+)?)     # 12, 12.5, 1.2e-3
    | (?P<ref>(?:'[^']+'!|[A-Za-z_][A-Za-z0-9_.]*!)?\$?[A-Za-z]{1,3}\$?\d+
              (?::\$?[A-Za-z]{1,3}\$?\d+)?)   # A1, $C$2, 'Read Me'!C27, C2:C15
    | (?P<func>[A-Za-z][A-Za-z0-9_.]*)        # EXP, SUM, ...
    | (?P<op>\*\*|[-+*/^(),])
    """,
    re.VERBOSE,
)

_PRECEDENCE = {"+": 1, "-": 1, "*": 2, "/": 2, "^": 3, "u-": 4}
_RIGHT_ASSOC: set = set()   # Excel evaluates ^ left-to-right


class ExprError(ValueError):
    """Raised when an expression cannot be parsed or evaluated."""


def tokenize(expr: str) -> List[Tuple[str, str]]:
    tokens: List[Tuple[str, str]] = []
    pos = 0
    expr = expr.strip()
    while pos < len(expr):
        if expr[pos].isspace():
            pos += 1
            continue
        m = _TOKEN_RE.match(expr, pos)
        if not m:
            raise ExprError("unrecognised character %r at position %d in %r"
                            % (expr[pos], pos, expr))
        kind = m.lastgroup
        text = m.group()
        if kind == "op" and text == "**":
            text = "^"
        tokens.append((kind, text))
        pos = m.end()
    return tokens


def evaluate_expression(expr: str, resolve: Callable[[str], Any]) -> float:
    """
    Evaluate an Excel-style arithmetic expression with correct BODMAS ordering.

    `resolve` is called with a cell reference or range string and must return a
    float (single cell) or a list of floats (a range).
    """
    tokens = tokenize(expr.lstrip("="))
    output: List[Any] = []          # value stack
    ops: List[str] = []             # operator / function stack
    argc: List[int] = []            # argument counters for functions

    def apply_op(op: str) -> None:
        if op == "u-":
            if not output:
                raise ExprError("unary minus with no operand in %r" % expr)
            output.append(-_scalar(output.pop()))
            return
        if len(output) < 2:
            raise ExprError("operator %r is missing an operand in %r" % (op, expr))
        b = _scalar(output.pop())
        a = _scalar(output.pop())
        if op == "+":
            output.append(a + b)
        elif op == "-":
            output.append(a - b)
        elif op == "*":
            output.append(a * b)
        elif op == "/":
            if b == 0:
                raise ExprError("division by zero in %r" % expr)
            output.append(a / b)
        elif op == "^":
            output.append(a ** b)
        else:
            raise ExprError("unknown operator %r" % op)

    def apply_func(name: str, args: List[Any]) -> None:
        flat: List[float] = []
        for a in args:
            if isinstance(a, list):
                flat.extend(float(x) for x in a)
            else:
                flat.append(_scalar(a))
        upper = name.upper()
        if upper == "EXP":
            output.append(math.exp(flat[0]))
        elif upper in ("LN", "LOG"):
            output.append(math.log(flat[0]))
        elif upper == "ABS":
            output.append(abs(flat[0]))
        elif upper == "SUM":
            output.append(sum(flat))
        elif upper == "MAX":
            output.append(max(flat))
        elif upper == "MIN":
            output.append(min(flat))
        elif upper == "POWER":
            output.append(flat[0] ** flat[1])
        elif upper == "SUMPRODUCT":
            if len(args) != 2:
                raise ExprError("SUMPRODUCT needs exactly 2 ranges")
            xs = args[0] if isinstance(args[0], list) else [args[0]]
            ys = args[1] if isinstance(args[1], list) else [args[1]]
            if len(xs) != len(ys):
                raise ExprError("SUMPRODUCT ranges differ in length (%d vs %d)"
                                % (len(xs), len(ys)))
            output.append(sum(float(x) * float(y) for x, y in zip(xs, ys)))
        else:
            raise ExprError("unsupported function %r" % name)

    prev_kind: Optional[str] = None
    prev_text: Optional[str] = None
    i = 0
    while i < len(tokens):
        kind, text = tokens[i]

        if kind == "num":
            output.append(float(text))

        elif kind == "ref":
            output.append(resolve(text))

        elif kind == "func":
            # A bare name followed by "(" is a function call.
            if i + 1 < len(tokens) and tokens[i + 1][1] == "(":
                ops.append("f:" + text)
                argc.append(1)
                ops.append("(")
                i += 2
                prev_kind, prev_text = "op", "("
                continue
            output.append(resolve(text))

        elif kind == "op":
            if text == "(":
                ops.append("(")
            elif text == ")":
                while ops and ops[-1] != "(":
                    apply_op(ops.pop())
                if not ops:
                    raise ExprError("unbalanced ')' in %r" % expr)
                ops.pop()  # discard "("
                if ops and ops[-1].startswith("f:"):
                    fname = ops.pop()[2:]
                    n = argc.pop()
                    args = [output.pop() for _ in range(n)][::-1]
                    apply_func(fname, args)
            elif text == ",":
                while ops and ops[-1] != "(":
                    apply_op(ops.pop())
                if argc:
                    argc[-1] += 1
            else:
                # Distinguish unary minus/plus from binary.
                unary = (
                    prev_kind is None
                    or (prev_kind == "op" and prev_text in ("(", ",", "+", "-", "*", "/", "^"))
                )
                if text == "-" and unary:
                    op = "u-"
                elif text == "+" and unary:
                    i += 1
                    prev_kind, prev_text = kind, text
                    continue
                else:
                    op = text
                while ops and ops[-1] not in ("(",) and not ops[-1].startswith("f:"):
                    top = ops[-1]
                    if (_PRECEDENCE[top] > _PRECEDENCE[op]) or (
                        _PRECEDENCE[top] == _PRECEDENCE[op] and op not in _RIGHT_ASSOC
                    ):
                        apply_op(ops.pop())
                    else:
                        break
                ops.append(op)

        prev_kind, prev_text = kind, text
        i += 1

    while ops:
        op = ops.pop()
        if op == "(" or op.startswith("f:"):
            raise ExprError("unbalanced '(' in %r" % expr)
        apply_op(op)

    if len(output) != 1:
        raise ExprError("expression %r did not reduce to a single value" % expr)
    return _scalar(output[0])


def _scalar(v: Any) -> float:
    if isinstance(v, list):
        if len(v) == 1:
            return float(v[0])
        raise ExprError("expected a single value, got a range of %d cells" % len(v))
    return float(v)


# --------------------------------------------------------------------------
# Recode rules
# --------------------------------------------------------------------------

_IF_PAIR_RE = re.compile(
    r"IF\(\s*\$?[A-Za-z]{1,3}\$?\d+\s*=\s*(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)\s*,",
    re.IGNORECASE,
)
_IF_TAIL_RE = re.compile(r",\s*(-?\d+(?:\.\d+)?)\s*\)+\s*$")
_PLAIN_REF_RE = re.compile(r"^=\s*\$?[A-Za-z]{1,3}\$?\d+\s*$")


@dataclass
class RecodeRule:
    """How a respondent's answer becomes the number fed into the SUMPRODUCT."""

    kind: str                                  # "identity" | "map"
    mapping: Dict[float, float] = field(default_factory=dict)
    default: float = 0.0
    source: str = ""

    @property
    def accepted(self) -> List[float]:
        return sorted(self.mapping)

    @property
    def is_binary_pair(self) -> bool:
        """A MaxDiff-style pair: original 1/2 collapsing to 1/0."""
        return self.kind == "map" and set(self.mapping) == {1.0, 2.0} and \
            set(self.mapping.values()) == {1.0, 0.0}

    def describe(self) -> str:
        if self.kind == "identity":
            return "pass-through (value used as-is)"
        pairs = ", ".join("%g->%g" % (k, self.mapping[k]) for k in self.accepted)
        return "%s, anything else -> %g" % (pairs, self.default)

    def apply(self, value: Any) -> Tuple[float, Optional[str]]:
        """Return (model_value, problem_flag_or_None)."""
        num = coerce_number(value)
        if num is None:
            # Blank / text / boolean-FALSE all behave as Excel does inside
            # SUMPRODUCT: they contribute nothing.
            return (self.default if self.kind == "map" else 0.0), "MISSING"
        if self.kind == "identity":
            return num, None
        if num in self.mapping:
            return self.mapping[num], None
        return self.default, "OUT_OF_RANGE"

    @classmethod
    def from_formula(cls, formula: Optional[str]) -> "RecodeRule":
        if formula is None:
            return cls(kind="identity", source="<no formula>")
        text = str(formula).strip()
        if not text.startswith("="):
            return cls(kind="identity", source=text)
        if _PLAIN_REF_RE.match(text):
            return cls(kind="identity", source=text)
        pairs = _IF_PAIR_RE.findall(text)
        if pairs:
            mapping = {float(a): float(b) for a, b in pairs}
            tail = _IF_TAIL_RE.search(text)
            default = float(tail.group(1)) if tail else 0.0
            return cls(kind="map", mapping=mapping, default=default, source=text)
        return cls(kind="identity", source=text)


def coerce_number(value: Any) -> Optional[float]:
    """
    Turn a cell value into a number the way Excel's SUMPRODUCT does.

    Blanks, text and logicals inside a SUMPRODUCT range count as zero, so they
    come back as None here and the caller decides what that means.  Numbers
    stored as text (the survey scripts hold coefficients as quoted strings) are
    converted, tolerating thousands separators and a decimal comma.
    """
    if value is None:
        return None
    if isinstance(value, bool):
        return None                     # Excel: logicals in a range -> 0
    if isinstance(value, (int, float)):
        if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
            return None
        return float(value)
    text = str(value).strip()
    if not text:
        return None
    text = text.strip('"').strip("'").strip()
    if not text:
        return None
    if re.fullmatch(r"-?\d{1,3}(?:,\d{3})+(?:\.\d+)?", text):
        text = text.replace(",", "")            # 1,234.56
    elif text.count(",") == 1 and "." not in text:
        text = text.replace(",", ".")           # 3,14 -> 3.14
    try:
        return float(text)
    except ValueError:
        return None


# --------------------------------------------------------------------------
# Model description
# --------------------------------------------------------------------------

@dataclass
class Variable:
    name: str
    label: str
    row: int
    coefficients: List[float]
    recode: RecodeRule
    is_constant: bool = False


@dataclass
class Model:
    source_file: str
    sheet: str
    segment_names: List[str]
    segment_columns: List[str]
    constant: List[float]
    variables: List[Variable]                      # predictors only, no constant
    input_column: str
    first_row: int
    last_row: int
    constant_row: Optional[int]
    phantom_columns: List[str] = field(default_factory=list)

    @property
    def n_segments(self) -> int:
        return len(self.segment_names)

    @property
    def n_variables(self) -> int:
        return len(self.variables)


_SUMPRODUCT_RE = re.compile(
    r"SUMPRODUCT\(\s*"
    r"(?:TRANSPOSE\(\s*)?"
    r"(?:'[^']+'!|[A-Za-z_][A-Za-z0-9_]*!)?"
    r"\$?([A-Za-z]{1,3})\$?(\d+)\s*:\s*\$?([A-Za-z]{1,3})\$?(\d+)"
    r"\)?\s*,\s*"
    r"(?:TRANSPOSE\(\s*)?"
    r"(?:'[^']+'!|[A-Za-z_][A-Za-z0-9_]*!)?"
    r"\$?([A-Za-z]{1,3})\$?(\d+)\s*:\s*\$?([A-Za-z]{1,3})\$?(\d+)"
    r"\)?\s*\)",
    re.IGNORECASE,
)

_SUM_RANGE_RE = re.compile(
    r"SUM\(\s*\$?([A-Za-z]{1,3})\$?(\d+)\s*:\s*\$?([A-Za-z]{1,3})\$?(\d+)\s*\)",
    re.IGNORECASE,
)


def cell_text(cell) -> Optional[str]:
    """Formula text for a cell, tolerating openpyxl's ArrayFormula wrapper."""
    v = cell.value
    if v is None:
        return None
    if hasattr(v, "text"):
        return str(v.text)
    return str(v)


_SIMPLE_REF_RE = re.compile(
    r"^=\s*(?:'([^']+)'|([A-Za-z_][A-Za-z0-9_ .]*))?!?\$?([A-Za-z]{1,3})\$?(\d+)\s*$"
)


def _resolved(ws_f, ws_v, coord: str, _depth: int = 0) -> Any:
    """
    Read a cell, following simple references so the answer is a real value.

    A workbook that Excel has calculated carries cached results, and those are
    used first.  A workbook that has only ever been written by a script has
    none, so a header like ='Read Me'!C27 would otherwise come back as its own
    formula text.  In that case the reference is followed by hand.
    """
    if ws_v is not None:
        v = ws_v[coord].value
        if v is not None and not (isinstance(v, str) and v.startswith("=")):
            return v

    text = cell_text(ws_f[coord])
    if text is None or not text.startswith("=") or _depth >= 8:
        return text

    m = _SIMPLE_REF_RE.match(text)
    if not m:
        return text
    quoted, bare, col, row = m.groups()
    target_sheet = quoted or bare
    wb_f = ws_f.parent
    wb_v = ws_v.parent if ws_v is not None else None
    if target_sheet:
        if target_sheet not in wb_f.sheetnames:
            return text
        nxt_f = wb_f[target_sheet]
        nxt_v = wb_v[target_sheet] if (wb_v is not None
                                       and target_sheet in wb_v.sheetnames) else None
    else:
        nxt_f, nxt_v = ws_f, ws_v
    return _resolved(nxt_f, nxt_v, "%s%s" % (col.upper(), row), _depth + 1)


def discover_model(path: str) -> Model:
    """Work out a typing tool's structure from its own formulas."""
    wb_f = openpyxl.load_workbook(path, data_only=False)
    try:
        wb_v = openpyxl.load_workbook(path, data_only=True)
    except Exception:
        wb_v = None

    # 1. Find every vertical SUMPRODUCT.  Vertical means the coefficient and
    #    input ranges each sit in a single column, which is the shape of the
    #    single-respondent calculation block; the per-row Batch formulas use a
    #    horizontal input range and are deliberately skipped here.
    candidates: Dict[Tuple[str, int], List[Tuple[str, str, int, int, str]]] = {}
    for ws in wb_f.worksheets:
        if ws.sheet_state != "visible" and ws.title.lower() != "formulas":
            pass  # hidden sheets are still worth scanning
        for row in ws.iter_rows():
            for cell in row:
                text = cell_text(cell)
                if not text or "SUMPRODUCT" not in text.upper():
                    continue
                m = _SUMPRODUCT_RE.search(text)
                if not m:
                    continue
                c1, r1, c2, r2, i1, ir1, i2, ir2 = m.groups()
                if c1.upper() != c2.upper() or i1.upper() != i2.upper():
                    continue                      # horizontal -> Batch style
                if (r1, r2) != (ir1, ir2):
                    continue                      # ranges must align row-for-row
                key = (ws.title, cell.row)
                candidates.setdefault(key, []).append(
                    (cell.coordinate, c1.upper(), int(r1), int(r2), i1.upper())
                )

    if not candidates:
        raise SystemExit(
            "Could not find a SUMPRODUCT-based scoring block in this workbook.\n"
            "Expected a sheet (usually called 'Formulas') with one\n"
            "=SUMPRODUCT(<coefficient column>, <input column>) per segment."
        )

    def rank(item):
        (sheet, row), hits = item
        return (1 if "formula" in sheet.lower() else 0, len(hits), -row)

    (sheet_name, score_row), hits = max(candidates.items(), key=rank)
    hits.sort(key=lambda h: column_index_from_string(h[1]))

    ws_f = wb_f[sheet_name]
    ws_v = wb_v[sheet_name] if wb_v is not None else None

    segment_columns = [h[1] for h in hits]
    first_row, last_row = hits[0][2], hits[0][3]
    input_column = hits[0][4]

    # 2. Header row holding the segment names: the nearest row above the
    #    coefficient block that is populated across the segment columns.
    segment_names: List[str] = []
    header_row = None
    for r in range(first_row - 1, 0, -1):
        vals = [_resolved(ws_f, ws_v, "%s%d" % (c, r)) for c in segment_columns]
        if sum(1 for v in vals if v not in (None, "")) >= max(1, len(vals) - 1):
            header_row = r
            segment_names = [
                str(v).strip() if v not in (None, "") else "seg%d" % (i + 1)
                for i, v in enumerate(vals)
            ]
            break
    if not segment_names:
        segment_names = ["seg%d" % (i + 1) for i in range(len(segment_columns))]

    # 3. Walk the coefficient block: constant row plus one row per predictor.
    constant_row: Optional[int] = None
    variables: List[Variable] = []
    constant: List[float] = [0.0] * len(segment_columns)

    for r in range(first_row, last_row + 1):
        name_raw = _resolved(ws_f, ws_v, "A%d" % r)
        label_raw = _resolved(ws_f, ws_v, "B%d" % r)
        name = "" if name_raw is None else str(name_raw).strip()
        label = "" if label_raw is None else str(label_raw).strip()

        coefs: List[float] = []
        for c in segment_columns:
            val = coerce_number(_resolved(ws_f, ws_v, "%s%d" % (c, r)))
            coefs.append(0.0 if val is None else val)

        input_cell = ws_f["%s%d" % (input_column, r)]
        input_formula = cell_text(input_cell)
        input_value = coerce_number(
            _resolved(ws_f, ws_v, "%s%d" % (input_column, r))
        )

        looks_constant = (
            name.lower() == "constant"
            or label.lower() == "constant"
            or (r == first_row and input_formula is not None
                and not str(input_formula).startswith("=") and input_value == 1)
        )
        if looks_constant and constant_row is None:
            constant_row = r
            constant = coefs
            continue

        if not name:
            name = "%s%d" % (input_column, r)
        variables.append(
            Variable(
                name=name,
                label=label,
                row=r,
                coefficients=coefs,
                recode=RecodeRule.from_formula(input_formula),
            )
        )

    if constant_row is None:
        warn("No 'constant' row found inside %s!%s%d:%s%d - the model will be "
             "scored WITHOUT an intercept, which is almost certainly wrong."
             % (sheet_name, segment_columns[0], first_row,
                segment_columns[-1], last_row))

    # 4. Probability denominator: does the SUM() span more columns than the
    #    model actually has coefficients for?
    phantom: List[str] = []
    last_seg_idx = column_index_from_string(segment_columns[-1])
    for row in ws_f.iter_rows(min_row=score_row, max_row=min(score_row + 30, ws_f.max_row)):
        for cell in row:
            text = cell_text(cell)
            if not text or "SUM(" not in text.upper():
                continue
            m = _SUM_RANGE_RE.search(text)
            if not m:
                continue
            c1, _r1, c2, _r2 = m.groups()
            end_idx = column_index_from_string(c2.upper())
            if end_idx > last_seg_idx:
                phantom = [
                    get_column_letter(i)
                    for i in range(last_seg_idx + 1, end_idx + 1)
                ]
            break
        if phantom:
            break

    wb_f.close()
    if wb_v is not None:
        wb_v.close()

    return Model(
        source_file=path,
        sheet=sheet_name,
        segment_names=segment_names,
        segment_columns=segment_columns,
        constant=constant,
        variables=variables,
        input_column=input_column,
        first_row=first_row,
        last_row=last_row,
        constant_row=constant_row,
        phantom_columns=phantom,
    )


# --------------------------------------------------------------------------
# Scoring
# --------------------------------------------------------------------------

EXP_LIMIT = 709.782712893384        # largest x where exp(x) is finite in float64


@dataclass
class Result:
    respondent: Any
    model_inputs: List[float]
    scores: List[float]
    exp_values: List[float]
    probabilities: List[float]       # percentages, sum to 100
    position: int                    # 1-based, matches MATCH(...,0)
    segment: str
    top_pct: float
    margin: float                    # top - runner-up, in percentage points
    flags: List[str]


def softmax_percent(scores: Sequence[float]) -> List[float]:
    """
    exp(score_i) / SUM(exp(score_j)) * 100, computed in a way that cannot
    overflow.

    Subtracting the maximum score before exponentiating is algebraically a
    no-op - the constant cancels between numerator and denominator - but it
    keeps every exponent at or below zero.  Excel computes EXP() first and
    fails with #NUM! once a score passes ~709; these models routinely produce
    scores of 30-110, and a wider questionnaire would push them past that.

    Note the order of operations: the division happens first and the scale to
    percent afterwards -> (exp_i / total) * 100, never exp_i / (total * 100).
    """
    if not scores:
        return []
    peak = max(scores)
    shifted = [math.exp(s - peak) for s in scores]
    total = sum(shifted)
    if total == 0:
        n = len(scores)
        return [100.0 / n] * n
    return [(s / total) * 100.0 for s in shifted]


def score_respondent(model: Model, raw: Dict[str, Any], respondent: Any = "",
                     assume_original_scale: Optional[bool] = None) -> Result:
    flags: List[str] = []
    missing: List[str] = []
    out_of_range: List[str] = []

    # --- step 1: raw answers -> model inputs -----------------------------
    model_inputs: List[float] = []
    for var in model.variables:
        value = raw.get(var.name.lower())
        rule_ = var.recode
        if (assume_original_scale is False and rule_.is_binary_pair
                and coerce_number(value) in (0.0, 1.0)):
            # Data already carries the recoded 0/1, so pass it straight through
            # rather than sending 0 through a map that only knows 1 and 2.
            model_value, problem = float(coerce_number(value)), None
        else:
            model_value, problem = rule_.apply(value)
        if problem == "MISSING":
            missing.append(var.name)
        elif problem == "OUT_OF_RANGE":
            out_of_range.append(var.name)
        model_inputs.append(model_value)

    # --- step 2: SUMPRODUCT, then the intercept --------------------------
    # Brackets first: every (coefficient * input) product is formed, those are
    # summed, and only then is the constant added once to the total.  Adding it
    # inside the loop would add it once per variable.
    scores: List[float] = []
    for s in range(model.n_segments):
        total = 0.0
        for var, x in zip(model.variables, model_inputs):
            total += (var.coefficients[s] * x)
        scores.append(total + model.constant[s])

    # --- steps 3 & 4: EXP, then normalise --------------------------------
    exp_values = [math.exp(s) if s <= EXP_LIMIT else math.inf for s in scores]
    if any(math.isinf(e) for e in exp_values):
        flags.append("EXCEL_OVERFLOW")
    probabilities = softmax_percent(scores)

    # --- step 5: highest position, first one wins on a tie ---------------
    best = max(probabilities)
    position = probabilities.index(best) + 1
    ordered = sorted(probabilities, reverse=True)
    runner_up = ordered[1] if len(ordered) > 1 else 0.0
    margin = best - runner_up

    if len(ordered) > 1 and abs(best - runner_up) < 1e-12:
        flags.append("TIE_FIRST_WINS")
    elif margin < 1.0:
        flags.append("LOW_MARGIN")
    if model_inputs and not any(x != 0 for x in model_inputs):
        # Nothing the respondent said survived the recode, so the scores are
        # just the intercepts and the "winner" is whichever segment has the
        # largest constant. Excel reports this with full confidence; it is not
        # a classification and should be treated as unclassifiable.
        flags.append("ALL_INPUTS_ZERO")
    if missing:
        flags.append("MISSING_INPUT(%s)" % ",".join(missing[:6]))
    if out_of_range:
        flags.append("OUT_OF_RANGE(%s)" % ",".join(out_of_range[:6]))

    return Result(
        respondent=respondent,
        model_inputs=model_inputs,
        scores=scores,
        exp_values=exp_values,
        probabilities=probabilities,
        position=position,
        segment=model.segment_names[position - 1],
        top_pct=best,
        margin=margin,
        flags=flags,
    )


def detect_original_scale(model: Model, rows: List[Dict[str, Any]]) -> Optional[bool]:
    """
    Decide whether incoming data is on the original answer scale or has already
    been recoded.

    The two are distinguishable because a MaxDiff pair is 1/2 in the original
    scale and 0/1 once recoded: a 2 can only be original, a 0 can only be
    recoded.  If a file shows neither, the question does not matter.
    """
    pair_vars = [v for v in model.variables if v.recode.is_binary_pair]
    if not pair_vars or not rows:
        return None
    saw_two = saw_zero = False
    for row in rows[:500]:
        for v in pair_vars:
            n = coerce_number(row.get(v.name.lower()))
            if n == 2.0:
                saw_two = True
            elif n == 0.0:
                saw_zero = True
    if saw_two and not saw_zero:
        return True
    if saw_zero and not saw_two:
        return False
    if saw_zero and saw_two:
        warn("Paired questions contain both 0 and 2, so the file mixes the "
             "original scale with already-recoded values. Treating it as the "
             "original scale; check the source data.")
        return True
    return None


# --------------------------------------------------------------------------
# Reading respondent data
# --------------------------------------------------------------------------

ID_HINTS = ("respondent", "cid", "id", "record", "caseid", "case", "uuid", "panelist")
TRUTH_HINTS = ("original", "actual", "true", "known", "hidsegment", "segment_original")


@dataclass
class Dataset:
    rows: List[Dict[str, Any]]
    ids: List[Any]
    truth: List[Optional[float]]
    source: str
    matched: List[str]
    unmatched: List[str]
    skipped_blank: int = 0


def _grid_from_excel(path: str, sheet: Optional[str]) -> List[Tuple[str, List[List[Any]]]]:
    wb = openpyxl.load_workbook(path, data_only=True, read_only=True)
    out = []
    for ws in wb.worksheets:
        if sheet and ws.title != sheet:
            continue
        grid = [list(r) for r in ws.iter_values() ] if hasattr(ws, "iter_values") else \
               [[c.value for c in r] for r in ws.iter_rows()]
        out.append((ws.title, grid))
    wb.close()
    return out


def _grid_from_csv(path: str) -> List[Tuple[str, List[List[Any]]]]:
    with open(path, "r", newline="", encoding="utf-8-sig", errors="replace") as fh:
        sample = fh.read(8192)
        fh.seek(0)
        try:
            dialect = csv.Sniffer().sniff(sample, delimiters=",;\t|")
        except csv.Error:
            dialect = csv.excel
        return [(os.path.basename(path), [row for row in csv.reader(fh, dialect)])]


def read_respondents(path: str, model: Model, sheet: Optional[str] = None) -> Dataset:
    """Locate the header row that names the model's variables and read below it."""
    ext = os.path.splitext(path)[1].lower()
    grids = _grid_from_csv(path) if ext in (".csv", ".txt", ".tsv") \
        else _grid_from_excel(path, sheet)

    wanted = {v.name.lower(): i for i, v in enumerate(model.variables)}
    best: Optional[Tuple[int, str, List[List[Any]], int, Dict[int, str]]] = None

    for title, grid in grids:
        for r_idx, row in enumerate(grid[:15]):
            colmap: Dict[int, str] = {}
            for c_idx, cell in enumerate(row):
                if cell is None:
                    continue
                key = str(cell).strip().lower()
                if key in wanted and key not in colmap.values():
                    colmap[c_idx] = key
            if len(colmap) > (best[0] if best else 0):
                best = (len(colmap), title, grid, r_idx, colmap)

    if not best or best[0] == 0:
        raise SystemExit(
            "None of the model's variable names were found as column headers in\n"
            "  %s\n"
            "Expected headers such as: %s"
            % (path, ", ".join(v.name for v in model.variables[:6]))
        )

    n_matched, title, grid, header_idx, colmap = best
    header = grid[header_idx]
    matched = [colmap[c] for c in sorted(colmap)]
    unmatched = [v.name for v in model.variables if v.name.lower() not in set(matched)]

    # Identify an ID column and, if present, a known-segment column for checking.
    id_col: Optional[int] = None
    truth_col: Optional[int] = None
    data_cols = set(colmap)
    for c_idx, cell in enumerate(header):
        if cell is None:
            continue
        key = str(cell).strip().lower()
        if id_col is None and c_idx not in data_cols and key in ID_HINTS:
            id_col = c_idx
        if truth_col is None and c_idx not in data_cols and key in TRUTH_HINTS:
            truth_col = c_idx
    if id_col is None:
        first_data = min(colmap) if colmap else 1
        id_col = 0 if first_data > 0 else None

    rows: List[Dict[str, Any]] = []
    ids: List[Any] = []
    truth: List[Optional[float]] = []
    skipped = 0
    for raw_row in grid[header_idx + 1:]:
        if not raw_row:
            continue
        rec = {colmap[c]: (raw_row[c] if c < len(raw_row) else None) for c in colmap}
        if all(v is None or str(v).strip() == "" for v in rec.values()):
            skipped += 1                               # blank row, as ISBLANK() guards
            continue
        rows.append(rec)
        ids.append(raw_row[id_col] if id_col is not None and id_col < len(raw_row) else len(rows))
        truth.append(coerce_number(raw_row[truth_col])
                     if truth_col is not None and truth_col < len(raw_row) else None)

    return Dataset(rows=rows, ids=ids, truth=truth,
                   source="%s [%s]" % (os.path.basename(path), title),
                   matched=matched, unmatched=unmatched, skipped_blank=skipped)


# --------------------------------------------------------------------------
# Reporting
# --------------------------------------------------------------------------

def print_model(model: Model) -> None:
    rule("MODEL STRUCTURE DETECTED")
    info("File            : %s" % os.path.basename(model.source_file))
    info("Scoring sheet   : %s   (block %s%d:%s%d, inputs in column %s)"
         % (model.sheet, model.segment_columns[0], model.first_row,
            model.segment_columns[-1], model.last_row, model.input_column))
    info("Segments        : %d" % model.n_segments)
    for i, (name, col) in enumerate(zip(model.segment_names, model.segment_columns), 1):
        info("   %2d. %-34s (column %s, constant %+.6f)"
             % (i, name, col, model.constant[i - 1]))
    info("Predictors      : %d" % model.n_variables)
    info("Intercept row   : %s"
         % ("row %d" % model.constant_row if model.constant_row else "NOT FOUND"))

    kinds: Dict[str, int] = {}
    for v in model.variables:
        kinds[v.recode.describe()] = kinds.get(v.recode.describe(), 0) + 1
    info("Recode rules    :")
    for desc, n in sorted(kinds.items(), key=lambda kv: -kv[1]):
        info("   %3d variable(s): %s" % (n, desc))

    if model.phantom_columns:
        warn("The probability denominator sums columns %s, which extend past the "
             "last segment with coefficients (%s). In Excel those blank cells "
             "count as 0, so the extra segment can never be assigned. If they "
             "are meant to be a reference category, rerun with "
             "--reference-segment."
             % (",".join(model.phantom_columns), model.segment_columns[-1]))


def print_variables(model: Model) -> None:
    rule("PREDICTORS AND COEFFICIENTS")
    head = "%-4s %-34s" % ("row", "variable")
    head += "".join("%12s" % n[:11] for n in model.segment_names)
    info(head)
    info("-" * len(head))
    if model.constant_row:
        line = "%-4d %-34s" % (model.constant_row, "constant")
        line += "".join("%12.5f" % c for c in model.constant)
        info(line)
    for v in model.variables:
        line = "%-4d %-34s" % (v.row, v.name[:34])
        line += "".join("%12.5f" % c for c in v.coefficients)
        info(line)


def print_audit(model: Model, res: Result) -> None:
    """Show the arithmetic for one respondent, in BODMAS order."""
    rule("CALCULATION AUDIT - respondent %s" % res.respondent)
    info("Order of operations: brackets -> exponent -> divide/multiply -> add/subtract\n")

    info("STEP 1  answers -> model inputs (recode)")
    info("  %-38s %8s   %s" % ("variable", "input", "rule"))
    for v, x in zip(model.variables, res.model_inputs):
        info("  %-38s %8g   %s" % (v.name[:38], x, v.recode.describe()))

    info("\nSTEP 2  SUMPRODUCT: sum of every (coefficient x input), then + constant")
    for s, name in enumerate(model.segment_names):
        terms = [(v.name, v.coefficients[s], x)
                 for v, x in zip(model.variables, res.model_inputs) if x != 0]
        body = " + ".join("(%.5f x %g)" % (c, x) for _n, c, x in terms[:6])
        if len(terms) > 6:
            body += " + ... (%d more non-zero terms)" % (len(terms) - 6)
        if not terms:
            body = "0"
        info("  %-22s = [ %s ]" % (name[:22], body))
        info("  %-22s   + (%.6f)  =  %.6f" % ("", model.constant[s], res.scores[s]))

    info("\nSTEP 3  EXP(score)")
    for s, name in enumerate(model.segment_names):
        e = res.exp_values[s]
        shown = "overflow (Excel would return #NUM!)" if math.isinf(e) else "%.6e" % e
        info("  EXP( %-26s %13.6f ) = %s" % (name[:26], res.scores[s], shown))

    info("\nSTEP 4  probability = ( EXP_i / SUM(EXP) ) x 100")
    info("        computed as a stabilised softmax so a large score cannot overflow")
    for s, name in enumerate(model.segment_names):
        info("  %-30s %9.5f %%" % (name[:30], res.probabilities[s]))
    info("  %-30s %9.5f %%" % ("TOTAL", sum(res.probabilities)))

    info("\nSTEP 5  MATCH(MAX(probabilities), probabilities, 0)")
    info("  highest value  : %.5f %%" % res.top_pct)
    info("  position       : %d of %d" % (res.position, model.n_segments))
    info("  segment        : %s" % res.segment)
    info("  margin over 2nd: %.5f percentage points" % res.margin)
    if res.flags:
        info("  flags          : %s" % "; ".join(res.flags))


# --------------------------------------------------------------------------
# Output
# --------------------------------------------------------------------------

def build_header(model: Model) -> List[str]:
    head = ["respondent"]
    head += ["in_" + v.name for v in model.variables]
    head += ["dfa_" + n for n in model.segment_names]
    head += ["pct_" + n for n in model.segment_names]
    head += ["position", "segment", "top_pct", "margin_pts", "flags"]
    return head


def build_row(res: Result) -> List[Any]:
    row: List[Any] = [res.respondent]
    row += res.model_inputs
    row += [round(s, 10) for s in res.scores]
    row += [round(p, 10) for p in res.probabilities]
    row += [res.position, res.segment, round(res.top_pct, 6),
            round(res.margin, 6), "; ".join(res.flags)]
    return row


def fmt_number(x: float, decimals: Optional[int] = None) -> str:
    """
    Plain digits, never scientific notation - the scripts cannot read 1e-05.

    With `decimals` set, the value is written to exactly that many places, which
    is how the existing hand-written scripts are formatted.  Left unset, the
    sheet's full precision is kept: a coefficient rounded to 4 places can move a
    borderline respondent into a different segment.
    """
    if decimals is not None:
        return "%.*f" % (min(decimals, 15), x)
    if x == int(x) and abs(x) < 1e15:
        return "%d.0" % int(x)
    out = repr(float(x))
    if "e" in out or "E" in out:
        out = "%.15f" % x
        out = out.rstrip("0")
        if out.endswith("."):
            out += "0"
    return out


def block_of(var: Variable) -> str:
    """Which question block a predictor belongs to, from its recode rule."""
    return "pair" if var.recode.is_binary_pair else "scale"


def parse_blocks(spec: str) -> List[Tuple[str, int]]:
    """Turn "TT2:16,TT1:8" into [("TT2",16),("TT1",8)], applied in sheet order."""
    out: List[Tuple[str, int]] = []
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if ":" not in part:
            raise SystemExit("--q-blocks needs NAME:COUNT entries, got %r" % part)
        name, _, count = part.partition(":")
        try:
            n = int(count)
        except ValueError:
            raise SystemExit("--q-blocks count must be a whole number, got %r" % count)
        out.append((name.strip(), n))
    return out


def assign_question_names(model: Model, prefixes: Dict[str, str],
                          blocks: Optional[List[Tuple[str, int]]] = None) -> List[str]:
    """
    Name every predictor's survey question.

    By default the recode rule decides the block, which separates rating items
    from paired items and matches the Sunoco and Signet scripts.  When two
    blocks share a recode rule that is not enough - Poppi's 16 MaxDiff items and
    8 semantic-differential items are all pass-through, yet the script names
    them TT2_1..16 and TT1_1..8 - so --q-blocks states the split outright.
    """
    if blocks:
        stated = sum(n for _n, n in blocks)
        if stated != model.n_variables:
            raise SystemExit(
                "--q-blocks covers %d variable(s) but the model has %d.\n"
                "The counts must add up, in sheet order." % (stated, model.n_variables))
        names: List[str] = []
        for prefix, count in blocks:
            names.extend("%s_%d" % (prefix, k) for k in range(1, count + 1))
        return names

    counters: Dict[str, int] = {}
    names = []
    for v in model.variables:
        b = block_of(v)
        counters[b] = counters.get(b, 0) + 1
        names.append("%s_%d" % (prefixes.get(b, b.upper()), counters[b]))
    return names


def generate_script(model: Model, prefixes: Dict[str, str], pair_style: str = "on",
                    condition: str = "'??STATUS?? has 2",
                    hidden_question: str = "HIDSegment",
                    reference: bool = False,
                    decimals: Optional[int] = None,
                    blocks: Optional[List[Tuple[str, int]]] = None,
                    assert_style: str = "check") -> str:
    """
    Write the survey-platform script that reproduces this model.

    The layout follows the reference scripts: build TempSeg from the answers,
    hold each segment's coefficients in a Seg<n> array, accumulate the
    SUMPRODUCT in a For loop, add the constants, exponentiate, convert to
    percentages and take IndexofMax.

    Predictors keep their sheet order, so a value's position in TempSeg always
    lines up with the same position in every Seg<n> array.  Question names are
    numbered within their own block, which is what the reference scripts do
    (QS17_1..3 for the scale items, QS16_1..10 for the pairs).
    """
    # A baseline segment has no coefficients of its own: it contributes a
    # trailing exp(0) = 1 term and nothing else, so it gets no Seg<n> array and
    # takes no part in the loop.  add_reference_segment() marks it with "-".
    real = [i for i, c in enumerate(model.segment_columns) if c != "-"]
    n_ref = model.n_segments - len(real)
    if reference and n_ref == 0:
        n_ref = 1
    n_seg = len(real)
    n_var = model.n_variables
    L: List[str] = []

    qname = assign_question_names(model, prefixes, blocks)

    L.append(condition)
    L.append("")
    L.append("' Generated from: %s" % os.path.basename(model.source_file))
    L.append("' Scoring block : %s!%s%d:%s%d"
             % (model.sheet, model.segment_columns[0], model.first_row,
                model.segment_columns[-1], model.last_row))
    L.append("' %d segments%s, %d predictors"
             % (n_seg + n_ref,
                " (%d scored + %d baseline)" % (n_seg, n_ref) if n_ref else "",
                n_var))
    L.append("'")
    L.append("' CHECK THE QUESTION NAMES BELOW before running. They are numbered")
    L.append("' per block; swap the prefixes for the real ones in your survey.")
    L.append("'")
    L.append("'   pos  script question        model variable")
    for i, (v, q) in enumerate(zip(model.variables, qname), 1):
        L.append("'   %-4d %-21s %s" % (i, q, v.name))
    L.append("")
    L.append("Dim i")
    L.append("Dim TempSeg = {}")
    L.append("Dim SegScore = {}")
    L.append("")

    helper: Dict[int, str] = {}
    if pair_style == "ifelse":
        pair_idx = [i for i, v in enumerate(model.variables) if block_of(v) == "pair"]
        if pair_idx:
            for n, i in enumerate(pair_idx, 1):
                helper[i] = "Seg%d" % (n_seg + n)
                L.append("Dim %s" % helper[i])
            L.append("")
            for i in pair_idx:
                L.append("If %s.answers.entrycode has {1} then" % qname[i])
                L.append("  %s=1" % helper[i])
                L.append("else")
                L.append("  %s=0" % helper[i])
                L.append("EndIf")
                L.append("")

    for i, v in enumerate(model.variables):
        if i in helper:
            expr = helper[i]
        elif block_of(v) == "pair":
            expr = ("on(%s.Answers.EntryCode has {1},1,"
                    "on(%s.Answers.EntryCode has {2},0))" % (qname[i], qname[i]))
        else:
            expr = "%s.Answers.EntryCode[1]" % qname[i]
        L.append("TempSeg.SetAt(%02d,%s)" % (i + 1, expr))
    L.append("")

    for k, sgi in enumerate(real, 1):
        vals = ";".join('"%s"' % fmt_number(v.coefficients[sgi], decimals)
                        for v in model.variables)
        L.append("Dim Seg%d = {%s}" % (k, vals))
    L.append("")

    for sgi in range(n_seg):
        L.append("SegScore.SetAt(%d,0)" % (sgi + 1))
    L.append("")
    L.append("Dim TempDrive = 0")
    L.append("")

    L.append("For i = 1 To %d" % n_var)
    for sgi in range(n_seg):
        L.append("  TempDrive = SegScore[%d] + (Seg%d[i].ToNumber() * TempSeg[i])"
                 % (sgi + 1, sgi + 1))
        L.append("  SegScore.SetAt(%d,TempDrive)" % (sgi + 1))
    L.append("Next i")
    L.append("")

    L.append("' add each segment's constant once, after the products are summed")
    for k, sgi in enumerate(real, 1):
        L.append("TempDrive = SegScore[%d] + (%s)"
                 % (k, fmt_number(model.constant[sgi], decimals)))
        L.append("SegScore.SetAt(%d,TempDrive)" % k)
    L.append("")

    total = n_seg + n_ref
    for k in range(1, n_seg + 1):
        L.append("dim fsum%d = pow(2.718281828,(SegScore[%d]))" % (k, k))
    for k in range(n_seg + 1, total + 1):
        L.append("' baseline segment: no coefficients, so its score is 0 and exp(0) = 1")
        L.append("dim fsum%d = 1" % k)
    L.append("")

    L.append("dim perc1={}")
    for k in range(total):
        L.append("perc1.InsertAt(%d,0)" % (k + 1))
    L.append("")
    L.append("dim finalSum = " + " + ".join("fsum%d" % (k + 1) for k in range(total)))
    L.append("")
    for k in range(total):
        L.append("perc1.SetAt(%d,(fsum%d/finalSum)*100)" % (k + 1, k + 1))
    L.append("")
    L.append("Dim SegmentFinal = perc1.IndexofMax()")
    L.append("")
    lhs = ("%s.hasnodata" % hidden_question if assert_style == "nodata"
           else "SegmentFinal = %s.Answers.EntryCode[1]" % hidden_question)
    L.append('Assert.Check(%s , "Segment1 Mismatch = " + SegmentFinal + "SP = " '
             '+ %s.Answers.EntryCode + "Score =" + perc1 + " - " + TempSeg '
             '+ "-" + SegScore)' % (lhs, hidden_question))
    L.append("")
    return "\n".join(L)


def write_outputs(model: Model, results: List[Result], data: "Dataset",
                  out_stem: str, script_text: str) -> List[str]:
    """
    One workbook and one script file.

    The workbook mirrors the layout of the source typing tools: a Batch tab
    with the raw inputs on the left, then DFA, EXP, Probability and Assignment
    blocks separated by a blank spacer column, exactly where they sit in the
    originals.
    """
    written: List[str] = []
    xlsx_path = out_stem + ".xlsx"
    script_path = out_stem + "_script.txt"

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Batch"
    names = model.segment_names
    n = model.n_segments

    # --- row 1: block banners, row 2: column names --------------------
    r1: List[Any] = [None, "RAW INPUTS"] + [None] * (model.n_variables - 1)
    r2: List[Any] = ["Respondent"] + [v.name for v in model.variables]

    def block(banner: str, headers: List[str]) -> None:
        r1.append(None); r2.append(None)                 # spacer column
        r1.append(banner); r1.extend([None] * (len(headers) - 1))
        r2.extend(headers)

    block("DFA", ["seg%d" % (i + 1) for i in range(n)])
    block("EXP", ["seg%d" % (i + 1) for i in range(n)])
    block("Probability", list(names))
    block("Assignment", ["Segment", "Name", "Top %", "Margin", "Flags"])
    ws.append(r1)
    ws.append(r2)

    for res in results:
        row: List[Any] = [res.respondent] + list(res.model_inputs)
        row.append(None); row.extend(res.scores)
        row.append(None)
        row.extend([e if not math.isinf(e) else "overflow" for e in res.exp_values])
        row.append(None); row.extend(res.probabilities)
        row.append(None)
        row.extend([res.position, res.segment, round(res.top_pct, 6),
                    round(res.margin, 6), "; ".join(res.flags)])
        ws.append(row)

    ws.freeze_panes = "B3"

    # --- supporting tabs ----------------------------------------------
    summary = wb.create_sheet("Summary")
    summary.append(["Segment", "Position", "Respondents", "Share %"])
    total = len(results) or 1
    counts = {i: 0 for i in range(1, n + 1)}
    for res in results:
        counts[res.position] += 1
    for i, name in enumerate(names, 1):
        summary.append([name, i, counts[i], round((counts[i] / total) * 100.0, 4)])
    summary.append(["Total", "", total, 100.0])
    summary.append([])
    summary.append(["Source model", os.path.basename(model.source_file)])
    summary.append(["Scoring sheet", model.sheet])
    summary.append(["Predictors", model.n_variables])
    summary.append(["Respondents", len(results)])
    summary.append(["Blank rows skipped", data.skipped_blank])
    summary.append(["Generated", _dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
    if WARNINGS:
        summary.append([])
        summary.append(["Warnings"])
        for wmsg in WARNINGS:
            summary.append([wmsg])

    msheet = wb.create_sheet("Model")
    msheet.append(["row", "variable", "label", "recode"] + names)
    if model.constant_row:
        msheet.append([model.constant_row, "constant", "constant", ""]
                      + list(model.constant))
    for v in model.variables:
        msheet.append([v.row, v.name, v.label, v.recode.describe()]
                      + list(v.coefficients))

    scr = wb.create_sheet("Script")
    scr.append(["The generated script is also saved as %s"
                % os.path.basename(script_path)])
    for line in script_text.split("\n"):
        scr.append([line])

    wb.save(xlsx_path)
    written.append(xlsx_path)

    with open(script_path, "w", encoding="utf-8") as fh:
        fh.write(script_text)
    written.append(script_path)
    return written


def add_reference_segment(model: Model, name: str = "reference") -> None:
    """
    Append a baseline segment whose coefficients are all zero.

    In a multinomial logit one category is usually left out and carries an
    implied score of 0, so its EXP is 1 and it competes with the rest.  The
    survey scripts do this (a trailing fsum term with no coefficients), while
    the workbooks leave the column blank, which makes it score 0 instead of 1.
    Use --reference-segment when the script's behaviour is the intended one.
    """
    model.segment_names.append(name)
    model.segment_columns.append("-")
    model.constant.append(0.0)
    for v in model.variables:
        v.coefficients.append(0.0)


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def run(model_path: str, data_path: Optional[str], out_path: Optional[str],
        sheet: Optional[str], audit: Optional[str], reference: bool,
        inspect_only: bool, show_vars: bool,
        prefixes: Optional[Dict[str, str]] = None,
        pair_style: str = "on", hidden_question: str = "HIDSegment",
        blocks: Optional[List[Tuple[str, int]]] = None,
        decimals: Optional[int] = None, assert_style: str = "check") -> int:
    prefixes = prefixes or {"scale": "TypingTool1DP", "pair": "TypingTool2DP"}
    if decimals is not None and decimals > 15:
        warn("--decimals %d exceeds what a 64-bit float can represent; "
             "capping at 15. Leave it unset to keep the sheet's own precision."
             % decimals)

    if not os.path.isfile(model_path):
        raise SystemExit("File not found: %s" % model_path)

    info("Reading model from: %s" % model_path)
    model = discover_model(model_path)
    if reference:
        add_reference_segment(model)
        info("Added an implicit zero-coefficient reference segment.")
    print_model(model)
    if show_vars:
        print_variables(model)
    if inspect_only:
        return 0

    source = data_path or model_path
    if data_path:
        info("\nReading respondents from: %s" % data_path)
    else:
        info("\nNo separate data file given - reading the workbook's own batch data.")
    data = read_respondents(source, model, sheet)

    rule("INPUT DATA")
    info("Source          : %s" % data.source)
    info("Respondents     : %d" % len(data.rows))
    if data.skipped_blank:
        info("Blank rows      : %d skipped (no answers in any model column)"
             % data.skipped_blank)
    info("Variables found : %d of %d" % (len(data.matched), model.n_variables))
    if data.unmatched:
        warn("No column found for %d variable(s): %s. They will be treated as "
             "unanswered, which contributes 0 to every segment."
             % (len(data.unmatched), ", ".join(data.unmatched[:8])))
    if not data.rows:
        raise SystemExit("No respondent rows to score.")

    original_scale = detect_original_scale(model, data.rows)
    if original_scale is True:
        info("Answer scale    : original (paired questions coded 1/2, recode applied)")
    elif original_scale is False:
        info("Answer scale    : already recoded (paired questions coded 0/1, passed through)")
    else:
        info("Answer scale    : not determinable from the data; recode rules applied as written")

    results = [
        score_respondent(model, row, rid, assume_original_scale=original_scale)
        for row, rid in zip(data.rows, data.ids)
    ]

    rule("SEGMENT ASSIGNMENT")
    total = len(results)
    counts = {i: 0 for i in range(1, model.n_segments + 1)}
    for res in results:
        counts[res.position] += 1
    info("%-4s %-34s %10s %9s" % ("pos", "segment", "count", "share"))
    for i, name in enumerate(model.segment_names, 1):
        info("%-4d %-34s %10d %8.2f%%"
             % (i, name[:34], counts[i], (counts[i] / total) * 100.0))
    info("%-4s %-34s %10d %8.2f%%" % ("", "TOTAL", total, 100.0))

    flagged = [r for r in results if r.flags]
    if flagged:
        tally: Dict[str, int] = {}
        for r in flagged:
            for f in r.flags:
                key = f.split("(")[0]
                tally[key] = tally.get(key, 0) + 1
        rule("QUALITY FLAGS")
        for key, n in sorted(tally.items(), key=lambda kv: -kv[1]):
            info("  %-22s %6d respondent(s)" % (key, n))

    checked = [(r, t) for r, t in zip(results, data.truth) if t is not None]
    if checked:
        hits = sum(1 for r, t in checked if r.position == int(t))
        rule("CHECK AGAINST THE FILE'S OWN SEGMENT COLUMN")
        info("  matched %d of %d  (%.2f%%)"
             % (hits, len(checked), (hits / len(checked)) * 100.0))
        if hits < len(checked):
            info("  first few mismatches:")
            shown = 0
            for r, t in checked:
                if r.position != int(t) and shown < 5:
                    info("    respondent %-14s expected %d, computed %d (%.4f%% vs %.4f%%)"
                         % (r.respondent, int(t), r.position,
                            r.probabilities[int(t) - 1] if 0 < int(t) <= model.n_segments else float("nan"),
                            r.top_pct))
                    shown += 1

    if audit:
        target = None
        if audit.lower() in ("first", "1st", ""):
            target = results[0]
        else:
            for r in results:
                if str(r.respondent).strip() == audit.strip():
                    target = r
                    break
        if target is None:
            warn("Respondent %r not found; auditing the first row instead." % audit)
            target = results[0]
        print_audit(model, target)

    if out_path is None:
        stem = os.path.splitext(os.path.basename(model_path))[0]
        out_path = os.path.join(os.path.dirname(os.path.abspath(model_path)),
                                "%s_results" % stem)

    script_text = generate_script(model, prefixes, pair_style=pair_style,
                                  hidden_question=hidden_question,
                                  reference=reference, decimals=decimals,
                                  blocks=blocks, assert_style=assert_style)
    rule("SCRIPT")
    qnames = assign_question_names(model, prefixes, blocks)
    seen: List[str] = []
    for q in qnames:
        stem = q.rsplit("_", 1)[0]
        if stem not in seen:
            seen.append(stem)
    for stem in seen:
        members = [q for q in qnames if q.rsplit("_", 1)[0] == stem]
        info("  %2d question(s): %s .. %s" % (len(members), members[0], members[-1]))
    info("  pair style   : %s" % pair_style)
    info("  coefficients : %s"
         % ("%d decimal places" % decimals if decimals is not None
            else "full precision from the sheet"))
    info("  check against: %s (%s)" % (hidden_question, assert_style))
    info("  %d lines generated" % len(script_text.split("\n")))

    written = write_outputs(model, results, data, out_path, script_text)
    rule("OUTPUT")
    for p in written:
        info("  wrote %s" % p)
    if WARNINGS:
        info("\n%d warning(s) were raised - see above and the Summary sheet." % len(WARNINGS))
    return 0


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(
        prog="segmentation_tool",
        description="Score respondents against a DFA / multinomial segmentation "
                    "typing tool workbook.",
    )
    ap.add_argument("model", nargs="?", help="the typing tool .xlsm/.xlsx file")
    ap.add_argument("data", nargs="?",
                    help="optional respondent file (.xlsx/.xlsm/.csv). "
                         "Defaults to the batch data inside the model workbook.")
    ap.add_argument("-o", "--out", help="output path stem (.xlsx and .csv are written)")
    ap.add_argument("-s", "--sheet", help="worksheet name inside the data file")
    ap.add_argument("-a", "--audit", nargs="?", const="first", metavar="ID",
                    help="print the full step-by-step arithmetic for one respondent")
    ap.add_argument("--reference-segment", action="store_true",
                    help="add an implicit zero-coefficient baseline segment "
                         "(matches the survey scripts' trailing exp(0) term)")
    ap.add_argument("--inspect", action="store_true",
                    help="describe the model structure and stop")
    ap.add_argument("--variables", action="store_true",
                    help="also print the full coefficient table")
    ap.add_argument("--q-scale", default="TypingTool1DP", metavar="NAME",
                    help="question name prefix for the rating/scale block "
                         "(default: TypingTool1DP)")
    ap.add_argument("--q-pair", default="TypingTool2DP", metavar="NAME",
                    help="question name prefix for the paired/MaxDiff block "
                         "(default: TypingTool2DP)")
    ap.add_argument("--pair-style", choices=("on", "ifelse"), default="on",
                    help="how paired questions are recoded in the script: a "
                         "nested on(...) expression, or an If/Else pre-pass")
    ap.add_argument("--hid", default="HIDSegment", metavar="NAME",
                    help="hidden question the script checks against "
                         "(default: HIDSegment)")
    ap.add_argument("--q-blocks", metavar="SPEC",
                    help="state the question blocks outright, in sheet order, "
                         "e.g. \"TT2:16,TT1:8\". Overrides --q-scale/--q-pair.")
    ap.add_argument("--decimals", type=int, metavar="N",
                    help="round coefficients to N places in the script "
                         "(default: the sheet's full precision)")
    ap.add_argument("--assert-style", choices=("check", "nodata"), default="check",
                    help="'check' compares against the hidden question, "
                         "'nodata' asserts it is empty (first deployment)")
    args = ap.parse_args(argv)

    model_path = args.model
    data_path = args.data

    if not model_path:                                  # double-clicked the .bat
        info("=" * 62)
        info(" SEGMENTATION TYPING TOOL")
        info("=" * 62)
        model_path = input("\nPath to the typing tool Excel file: ").strip().strip('"')
        if not model_path:
            info("Nothing entered - exiting.")
            return 1
        extra = input("Path to a separate respondent file (Enter to use the "
                      "workbook's own batch data): ").strip().strip('"')
        data_path = extra or None

    try:
        code = run(model_path, data_path, args.out, args.sheet, args.audit,
                   args.reference_segment, args.inspect, args.variables,
                   prefixes={"scale": args.q_scale, "pair": args.q_pair},
                   pair_style=args.pair_style, hidden_question=args.hid,
                   blocks=parse_blocks(args.q_blocks) if args.q_blocks else None,
                   decimals=args.decimals, assert_style=args.assert_style)
    except SystemExit as exc:
        info("\nERROR: %s" % exc)
        code = 2
    except Exception as exc:
        info("\nUNEXPECTED ERROR: %s: %s" % (type(exc).__name__, exc))
        code = 3

    if not args.model and sys.stdin.isatty():
        try:
            input("\nPress Enter to close...")
        except EOFError:
            pass
    return code


if __name__ == "__main__":
    sys.exit(main())
