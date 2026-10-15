"""Isolate private web data while preserving desktop owner zero."""
from alembic import op
import sqlalchemy as sa

revision = "0031"
down_revision = "0030"
branch_labels = None
depends_on = None

PRIVATE_TABLES = ('papers', 'paper_source_records', 'paper_visuals', 'paper_chunks', 'paper_claims', 'claim_evidence', 'knowledge_conversations', 'knowledge_conversation_turns', 'saved_comparisons', 'paper_visual_crops', 'analyses', 'paper_parse_runs', 'paper_page_extractions', 'scientific_datasets', 'scientific_analysis_runs', 'notes', 'user_settings', 'task_runs', 'contest_projects', 'contest_sources', 'contest_rules', 'contest_rubric_items', 'contest_milestones', 'contest_rubric_checks', 'contest_defense_sessions', 'contest_defense_turns', 'scientific_imports', 'research_ideas', 'experiment_designs', 'research_exports', 'learning_packs', 'learning_pack_sources', 'learning_cards', 'learning_questions', 'learning_attempts', 'learning_weaknesses', 'learning_plans', 'learning_plan_tasks', 'learning_review_states', 'learning_review_events', 'research_subscriptions', 'research_runs', 'research_recommendations', 'research_notifications', 'paper_glossaries')


def upgrade():
    for table in PRIVATE_TABLES:
        op.add_column(table, sa.Column("user_id", sa.Integer(), nullable=False, server_default="0"))
        op.create_index(f"ix_{table}_user_id", table, ["user_id"])
    # Original unique indices/constraints must include the owner.
    inspector = sa.inspect(op.get_bind())
    naming = {"uq": "uq_%(table_name)s_%(column_0_name)s"}
    for table, fields in (("papers", ("file_hash", "doi", "arxiv_id")), ("scientific_imports", ("sha256",)), ("paper_source_records", ())):
        with op.batch_alter_table(table, naming_convention=naming) as batch:
            for index in inspector.get_indexes(table):
                if index.get("unique") and index["column_names"] in [[f] for f in fields]:
                    batch.drop_index(index["name"])
                    batch.create_index(index["name"], index["column_names"], unique=False)
            for constraint in inspector.get_unique_constraints(table):
                cols = constraint["column_names"]
                if cols in [[f] for f in fields] or (table == "paper_source_records" and cols == ["source", "external_id"]):
                    name = constraint["name"] or f"uq_{table}_{cols[0]}"
                    batch.drop_constraint(name, type_="unique")
            if table == "papers":
                for field in fields:
                    batch.create_unique_constraint(f"uq_papers_owner_{field}", ["user_id", field])
            elif table == "scientific_imports":
                batch.create_unique_constraint("uq_scientific_imports_owner_hash", ["user_id", "sha256"])
            else:
                batch.create_unique_constraint("uq_paper_source_records_source_external_id", ["user_id", "source", "external_id"])


def downgrade():
    # Reverting to shared uniqueness can destroy multi-user semantics. Restore
    # a compatible pre-upgrade backup instead of silently merging private rows.
    raise RuntimeError("Restore the pre-web backup to downgrade ownership")
