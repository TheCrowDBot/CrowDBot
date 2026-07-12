import streamlit as st
from crowdbot.services.pipeline_queue import advance


class PipelineRunner:

    def __init__(self, pipelines):
        self.pipelines = pipelines

    def run(self, context):

        step = st.session_state.get(
            "pipeline_step",
            0,
        )

        if step >= len(self.pipelines):

            # finished current image
            st.session_state.pipeline_step = 0

            # move to next image
            advance()

            st.session_state.pop(
                "pipeline_context",
                None,
            )

            if st.session_state.auto_run:
                st.rerun()

            return context

        pipeline = self.pipelines[step]

        result = pipeline.run(**context)

        context[pipeline.name] = result

        st.session_state.pipeline_context = context
        st.session_state.pipeline_step = step + 1

        # Last pipeline finished
        if st.session_state.pipeline_step >= len(self.pipelines):
            st.session_state.pipeline_step = 0

            advance()

            st.session_state.pop(
                "pipeline_context",
                None,
            )

        if st.session_state.auto_run:
            st.rerun()

        return context
