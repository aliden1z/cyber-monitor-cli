# Cyber Monitor CLI - Installation Script
# Installs dependencies into an isolated virtual environment

INSTALL_DIR = /opt/cyber-monitor
BIN_DIR = /usr/local/bin
EXEC_NAME = cyber-monitor

install:
	@echo "🚀 Installing Cyber Monitor CLI..."
	
	# 1. Create installation directory and copy source files
	@mkdir -p $(INSTALL_DIR)
	@cp monitor.py $(INSTALL_DIR)/
	@cp requirements.txt $(INSTALL_DIR)/
	
	# 2. Create an isolated Virtual Environment (Venv)
	@echo "📦 Creating virtual environment and installing dependencies..."
	@python3 -m venv $(INSTALL_DIR)/venv
	
	# 3. Install required libraries (rich, psutil) into the venv
	@$(INSTALL_DIR)/venv/bin/pip install -q -r $(INSTALL_DIR)/requirements.txt
	
	# 4. Create the global executable wrapper script
	@echo "#!/bin/bash" > $(BIN_DIR)/$(EXEC_NAME)
	@echo "$(INSTALL_DIR)/venv/bin/python $(INSTALL_DIR)/monitor.py \"\$$@\"" >> $(BIN_DIR)/$(EXEC_NAME)
	
	# 5. Set executable permissions
	@chmod +x $(BIN_DIR)/$(EXEC_NAME)
	
	@echo "✅ Success! Type '$(EXEC_NAME)' to start monitoring."

uninstall:
	@echo "🗑️ Removing Cyber Monitor CLI..."
	@rm -rf $(INSTALL_DIR)
	@rm -f $(BIN_DIR)/$(EXEC_NAME)
	@echo "✅ Uninstalled successfully."
