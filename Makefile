SESSIONS := session_01 session_02 session_03 session_04 session_05 \
            session_06 session_07 session_08 session_09 session_10 \
            session_11 session_12 session_13 session_14 session_15

.PHONY: clean help $(addprefix clean-,$(SESSIONS))

## Remove all generated artifacts from every session (restores freshly-cloned state)
clean: $(addprefix clean-,$(SESSIONS))
	@echo "All sessions cleaned."

define clean_session
.PHONY: clean-$(1)
clean-$(1):
	@echo "Cleaning $(1)..."
	rm -rf $(1)/.venv
	find $(1) -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	find $(1) -name ".pytest_cache" -type d -exec rm -rf {} + 2>/dev/null || true
	find $(1) -name "*.pyc" -delete 2>/dev/null || true
	find $(1) -name "*.log" -delete 2>/dev/null || true
	rm -f $(1)/db.sqlite3
endef

$(foreach session,$(SESSIONS),$(eval $(call clean_session,$(session))))

# Extra: remove generated gRPC stubs from session_12
clean-session_12: clean-session_12-proto
clean-session_12-proto:
	rm -f session_12/service_pb2.py session_12/service_pb2_grpc.py

## Show available targets
help:
	@echo "Usage:"
	@echo "  make clean              Remove all generated artifacts from all sessions"
	@echo "  make clean-session_XX   Remove artifacts from a specific session"
	@echo ""
	@echo "Available sessions: $(SESSIONS)"
