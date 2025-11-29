# Cyber Monitor CLI - Makefile
# System-wide installation script

INSTALL_DIR = /opt/cyber-monitor
BIN_DIR = /usr/local/bin
EXEC_NAME = cyber-monitor
PYTHON = python3

.PHONY: install uninstall clean

install:
	@echo "[*] Installing Cyber Monitor CLI..."

	@# 1. Prepare directories
	@echo "    -> Creating installation directory: $(INSTALL_DIR)"
	@mkdir -p $(INSTALL_DIR)
	@cp monitor.py $(INSTALL_DIR)/
	@cp requirements.txt $(INSTALL_DIR)/

	@# 2. Setup Virtual Environment
	@echo "    -> Creating isolated virtual environment..."
	@$(PYTHON) -m venv $(INSTALL_DIR)/venv

	@# 3. Install Dependencies
	@echo "    -> Installing dependencies (rich, psutil)..."
	@$(INSTALL_DIR)/venv/bin/pip install -q --upgrade pip
	@$(INSTALL_DIR)/venv/bin/pip install -q -r $(INSTALL_DIR)/requirements.txt

	@# 4. Create Wrapper Script
	@echo "    -> Creating executable wrapper at $(BIN_DIR)/$(EXEC_NAME)"
	@echo "#!/bin/bash" > $(BIN_DIR)/$(EXEC_NAME)
	@echo "exec $(INSTALL_DIR)/venv/bin/python $(INSTALL_DIR)/monitor.py \"\$$@\"" >> $(BIN_DIR)/$(EXEC_NAME)

	@# 5. Permissions
	@chmod +x $(BIN_DIR)/$(EXEC_NAME)

	@echo "[+] Installation complete."
	@echo "    Run '$(EXEC_NAME)' to start the dashboard."

uninstall:
	@echo "[*] Uninstalling Cyber Monitor CLI..."
	@rm -rf $(INSTALL_DIR)
	@rm -f $(BIN_DIR)/$(EXEC_NAME)
	@echo "[-] System cleaned. Uninstallation successful."
