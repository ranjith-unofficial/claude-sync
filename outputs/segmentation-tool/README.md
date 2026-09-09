# Segmentation Typing Tool

Point it at a DFA / multinomial "typing tool" workbook. It reads the workbook's
own formulas to work out the structure, then produces **two things**:

1. **One Excel file** — a `Batch` tab with the raw inputs plus the DFA scores,
   EXP values, probabilities and segment assignment, laid out like the source
   workbooks.
2. **The segmentation script** — ready to paste into the survey platform.

The workbook you feed it only needs the **Formulas** tab (coefficients and
recode rules) and a **Batch** tab holding *raw inputs only*. Everything
downstream — SUMPRODUCT, EXP, percentages, the winning position — is calculated
here; none of it has to exist in the file already.

Verified against all three source workbooks: **9,854 respondents, every segment
assignment identical to the workbook's own answer**, DFA scores matching to the
last bit and probabilities to within 6e-14 (floating-point noise).

---

## Running it

**Easiest:** drag the Excel file onto `RUN_SEGMENTATION.bat`.

**Or** double-click `RUN_SEGMENTATION.bat` and paste the path when asked.

The `.bat` finds Python, installs `openpyxl` if it is missing, asks for the
survey question names, and runs the engine. Two files land next to the Excel
file:

| File | Contents |
|---|---|
| `<name>_results.xlsx` | `Batch` tab with the results, plus `Summary`, `Model` and `Script` tabs |
| `<name>_results_script.txt` | The segmentation script |

Both files must stay in the same folder. Python 3.7+ is required — install from
python.org and tick *"Add python.exe to PATH"*.

### From the command line

```
python segmentation_tool.py "Sunoco Typing Tool.xlsm"
python segmentation_tool.py "Sunoco Typing Tool.xlsm" fieldwork.csv -o results
python segmentation_tool.py "Poppi Typing Tool v2.xlsm" --inspect
python segmentation_tool.py "Signet Typing Tool.xlsm" --audit 809800089
```

| Option | What it does |
|---|---|
| *(second path)* | Score a separate `.xlsx` / `.xlsm` / `.csv` of responses instead of the workbook's own Batch tab |
| `-o`, `--out` | Output path stem; `.xlsx` and `.csv` are both written |
| `-s`, `--sheet` | Worksheet name inside the data file |
| `-a`, `--audit [ID]` | Print the full step-by-step arithmetic for one respondent |
| `--inspect` | Describe the detected structure and stop |
| `--variables` | Print the whole coefficient table |
| `--reference-segment` | Add an implicit zero-coefficient baseline segment (see below) |
| `--q-scale NAME` | Question prefix for the rating/scale block (default `TypingTool1DP`) |
| `--q-pair NAME` | Question prefix for the paired/MaxDiff block (default `TypingTool2DP`) |
| `--q-blocks SPEC` | State the split outright in sheet order, e.g. `TT2:16,TT1:8` |
| `--pair-style on\|ifelse` | Paired questions as a nested `on(...)` or an `If/Else` pre-pass |
| `--hid NAME` | Hidden question the script checks against (default `HIDSegment`) |
| `--assert-style check\|nodata` | Compare against the hidden question, or assert it is empty |
| `--decimals N` | Round coefficients to N places (default: the sheet's full precision) |

### Reproducing the three reference scripts

```
python segmentation_tool.py "Sunoco Typing Tool.xlsm" ^
    --q-scale QS17 --q-pair QS16 --pair-style ifelse ^
    --decimals 4 --assert-style nodata

python segmentation_tool.py "Signet Typing Tool.xlsm"

python segmentation_tool.py "Poppi Typing Tool v2.xlsm" ^
    --q-blocks "TT2:16,TT1:8" --reference-segment
```

---

## The generated script

Same shape as the hand-written ones: build `TempSeg` from the answers, hold each
segment's coefficients in a `Seg<n>` array, accumulate the SUMPRODUCT in a `For`
loop, add the constants, exponentiate, convert to percentages, `IndexofMax`.

Predictors keep their sheet order, so a value's position in `TempSeg` always
lines up with the same position in every `Seg<n>` array.

**Question names are the one thing that cannot be read out of the Excel** — the
Formulas tab holds model variable names (`x10x19`, `v7`), not survey question
IDs (`QS16_4`, `TT2_1`). They are numbered per block and the script carries a
mapping table in its header comments, so check that block before running.

Blocks are worked out from the recode rules: rating items in one, paired items
in the other. When both blocks share a recode rule — Poppi's 16 MaxDiff and 8
semantic-differential items are all pass-through — use `--q-blocks` to state the
split.

### Verified against the reference scripts

| Script | Lines generated | vs reference | Coefficients |
|---|---|---|---|
| Sunoco | 128 | 128/128 identical | exact |
| Signet | 93 | 93/93 identical | exact |
| Poppi | 82 | 82/82 identical | exact |

Every number in the generated scripts is bit-identical to the hand-written ones
(max difference 0.00e+00). The references pad trailing zeros (`"3.8771760"`);
this writes the same value unpadded (`"3.877176"`) unless `--decimals` is given.

**Round trip:** feeding each generated script's own numbers back over the batch
data reproduces the workbook's segment for **9,854 of 9,854 respondents**.

---

## What it calculates

The same five steps the workbooks and the survey scripts both implement:

| Step | Excel | Here |
|---|---|---|
| 1 | recode formulas in the INPUT column | parsed out of the sheet, per variable |
| 2 | `SUMPRODUCT(coefficients, inputs)` | sum of `(coefficient × input)`, then `+ constant` |
| 3 | `EXP(score)` | same |
| 4 | `EXP_i / SUM(EXP) * 100` | stabilised softmax, mathematically identical |
| 5 | `MATCH(MAX(probs), probs, 0)` | first-highest position, then the segment name |

The `constant` row is part of the SUMPRODUCT with an input of 1, so the
intercept is added exactly once. Dropping it changes every answer.

Nothing about the layout is assumed. The engine finds the SUMPRODUCT formulas
and reads the column letters, row span, recode rules and segment names back out
of them, so 5-, 6-, 7- or n-segment models all work unchanged.

---

## Order of operations

All arithmetic is explicitly parenthesised. The traps that matter here:

- `(exp_i / total) × 100`, never `exp_i / (total × 100)` — wrong by 10,000×.
- Every `(coefficient × input)` product is formed first, those are summed, and
  the constant is added **once to the total** — not once per variable.
- `exp(a) / sum` is not `exp(a / sum)`.
- Negative coefficients (Signet has one, `-0.5485032`) carry a unary minus,
  not a subtraction.

For any workbook whose formulas differ from the recognised shapes, the engine
falls back to a proper tokeniser and shunting-yard evaluator rather than
guessing. It follows **Excel's** precedence, which departs from textbook BODMAS
in two places:

- `-2^2` is **4** in Excel, −4 by textbook convention (unary minus binds tighter).
- `2^3^2` is **64** in Excel, 512 by textbook convention (`^` is left-associative).

Neither shape appears in the scoring chain, so neither ever changes a segment —
they are handled so a workbook variant is still read the way Excel reads it.

---

## Edge cases handled

| Case | Behaviour |
|---|---|
| **Score too large for `EXP()`** | Excel returns `#NUM!` above ~709.78. The stabilised softmax subtracts the peak score first, so it cannot overflow. Flagged `EXCEL_OVERFLOW`. |
| **Blank / text / `FALSE` answers** | Count as zero, exactly as they do inside a SUMPRODUCT range. Flagged `MISSING_INPUT`. |
| **Answers outside the valid set** | Fall to the recode's `else` value. Flagged `OUT_OF_RANGE`. |
| **Every input resolves to 0** | Scores collapse to the intercepts and the "winner" is just whichever segment has the largest constant. Excel reports this at 99.99% confidence. Flagged `ALL_INPUTS_ZERO` — treat as unclassifiable. |
| **Blank rows** | Skipped and counted, matching the `IF(ISBLANK(...),"")` guard. |
| **Tied probabilities** | First position wins, matching `MATCH(...,0)`. Flagged `TIE_FIRST_WINS`. |
| **Near-ties** | Flagged `LOW_MARGIN` when the top two are within 1 percentage point. |
| **Original vs recoded scale** | Auto-detected: a paired question coded `2` can only be the original scale, `0` can only be already-recoded. |
| **Missing columns** | Reported by name, then treated as unanswered. |
| **Numbers stored as text** | Converted, tolerating thousands separators and a decimal comma. |
| **Ranges of unequal length** | Rejected rather than silently truncated (Excel gives `#VALUE!`). |

---

## The reference-segment question

The **Poppi** workbook names six segments but only carries coefficients for
five. Its probability denominator is `SUM(C30:H30)` — one column wider than the
model. In Excel that blank column counts as **0**, so seg6 can never be
assigned.

The matching survey script has a trailing `fsum6 = pow(e, SegScore[6])` where
`SegScore[6]` is never set. If that reads as 0, `exp(0)` is **1**, and seg6
competes with the rest.

So the workbook and the script disagree. On the real 2,404-respondent file it
makes no difference — the genuine scores are large enough that `exp(0) = 1` never
wins. It only bites on a respondent with no usable answers:

- workbook: **seg3 at 99.999975%**
- script: **seg6 at 100%**

Both are artefacts, which is what `ALL_INPUTS_ZERO` is for. The tool follows the
workbook by default and warns; pass `--reference-segment` to follow the script.

---

## Output

One workbook, four tabs:

- **Batch** — raw inputs, then DFA / EXP / Probability / Assignment blocks,
  separated by spacer columns exactly as the source workbooks lay them out.
  Assignment carries the position, segment name, top %, margin over the
  runner-up and any quality flags.
- **Summary** — segment sizes and shares, plus any warnings raised.
- **Model** — the full coefficient table and recode rule for every variable.
- **Script** — the same script that is written to the `.txt`.

If the input file carries a known-segment column (`Original`, `Actual`, …), the
run also reports how often the computed segment matches it.
