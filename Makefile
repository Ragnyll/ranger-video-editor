PLUGIN_DIR=$(if $(XDG_CONFIG_HOME),$(XDG_CONFIG_HOME),$(HOME)/.config)/ranger/plugins

install:
	install -Dm644 video_editor.py $(PLUGIN_DIR)/video_editor.py

uninstall:
	$(RM) $(PLUGIN_DIR)/video_editor.py
