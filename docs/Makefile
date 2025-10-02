# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# Custom targets for Baobab Automata documentation

# Generate API documentation
api:
	@echo "Generating API documentation..."
	@$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	@echo "API documentation generated in $(BUILDDIR)/html/"

# Clean build directory
clean:
	@echo "Cleaning build directory..."
	@rm -rf $(BUILDDIR)/*
	@echo "Build directory cleaned."

# Build documentation for different formats
html:
	@$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

pdf:
	@$(SPHINXBUILD) -M latexpdf "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

epub:
	@$(SPHINXBUILD) -M epub "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# Serve documentation locally
serve: html
	@echo "Starting local server..."
	@cd $(BUILDDIR)/html && python -m http.server 8000
	@echo "Documentation available at http://localhost:8000"

# Check for broken links
linkcheck:
	@$(SPHINXBUILD) -M linkcheck "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# Check spelling
spelling:
	@$(SPHINXBUILD) -M spelling "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# Build all formats
all: html pdf epub
	@echo "All documentation formats built successfully."

# Install dependencies for documentation
install-deps:
	@echo "Installing documentation dependencies..."
	@pip install sphinx sphinx-rtd-theme sphinx-autodoc-typehints

# Update version information
update-version:
	@echo "Updating version information..."
	@python -c "import sys; sys.path.insert(0, '../src'); from baobab_automata import __version__; print(__version__)" > version.txt
	@echo "Version updated."

# Generate changelog
changelog:
	@echo "Generating changelog..."
	@python ../scripts/generate_changelog.py > changelog.rst
	@echo "Changelog generated."

# Full documentation build
docs: install-deps update-version changelog html
	@echo "Full documentation build completed."
	@echo "Documentation available in $(BUILDDIR)/html/"

# Development documentation (with auto-reload)
dev: html
	@echo "Starting development server with auto-reload..."
	@$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O) -a
	@echo "Development documentation ready."

# Test documentation
test-docs: html
	@echo "Testing documentation..."
	@python -m pytest ../tests/test_documentation.py -v
	@echo "Documentation tests completed."

# Deploy documentation (placeholder)
deploy:
	@echo "Deploying documentation..."
	@echo "This would typically deploy to GitHub Pages or Read the Docs"
	@echo "Deployment not configured yet."

# Show documentation statistics
stats:
	@echo "Documentation statistics:"
	@echo "Source files: $$(find . -name '*.rst' | wc -l)"
	@echo "Python files documented: $$(find ../src -name '*.py' | wc -l)"
	@echo "Examples: $$(find examples -name '*.rst' | wc -l)"
	@echo "API modules: $$(find api -name '*.rst' | wc -l)"