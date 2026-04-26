# Sweet Trap v4 — manuscript compile pipeline (md → docx/pdf)
# Usage:
#   make           # build manuscript.docx (default target)
#   make pdf       # build manuscript.pdf  (requires xelatex)
#   make html      # build manuscript.html (self-contained)
#   make lint      # run pre-submission-lint (CJK/section/table orphan)
#   make all       # build docx + pdf + html
#   make clean     # remove generated artifacts
#
# Dependencies: pandoc >= 3, pandoc-crossref (optional, for @fig:X refs),
# citeproc (built-in to pandoc), xelatex for PDF.

SRC       := manuscript.md
BIB       := references.bib
CSL       := templates/elife.csl
OUT_DOCX  := manuscript.docx
OUT_PDF   := manuscript.pdf
OUT_HTML  := manuscript.html
LINT      := ../../_meta/scripts/pre-submission-lint.py

PANDOC_OPTS := \
	--from markdown+yaml_metadata_block+pipe_tables+fenced_divs+bracketed_spans \
	--filter pandoc-crossref \
	--citeproc \
	--bibliography=$(BIB) \
	--csl=$(CSL) \
	--metadata link-citations=true \
	--metadata figureTitle="Figure" \
	--metadata tableTitle="Table" \
	--resource-path=.:figs

.PHONY: default all pdf html lint clean

default: $(OUT_DOCX)

all: $(OUT_DOCX) $(OUT_PDF) $(OUT_HTML)

$(OUT_DOCX): $(SRC) $(BIB) $(CSL)
	pandoc $(PANDOC_OPTS) \
		-o $@ $(SRC)
	@echo "Built: $@"

$(OUT_PDF): $(SRC) $(BIB) $(CSL)
	pandoc $(PANDOC_OPTS) \
		--pdf-engine=xelatex \
		-V mainfont="Helvetica Neue" \
		-V geometry:margin=2cm \
		-o $@ $(SRC)
	@echo "Built: $@"

$(OUT_HTML): $(SRC) $(BIB) $(CSL)
	pandoc $(PANDOC_OPTS) \
		--standalone \
		--mathjax \
		-o $@ $(SRC)
	@echo "Built: $@"

lint: $(SRC)
	@if [ -f $(LINT) ]; then \
		python3 $(LINT) $(SRC); \
	else \
		echo "pre-submission-lint.py not found at $(LINT)"; \
		exit 1; \
	fi

clean:
	rm -f $(OUT_DOCX) $(OUT_PDF) $(OUT_HTML)

# Helper: word count excluding YAML front matter + references
wc:
	@awk '/^---$$/{f=!f;next}!f' $(SRC) | wc -w
