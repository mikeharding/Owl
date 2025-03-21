import streamlit as st

import sskeys as kz
import owlbridge as owb


ret = kz.titleBar("Graphs")

if ret is None or kz.caseHasNoPlan():
    st.info("Case(s) must be first created before running this page.")
else:
    if kz.caseIsRunReady():
        owb.runPlan()

    st.write("Optimize a single scenario based on the parameters selected in the **Case Setup** section.")
    col1, col2 = st.columns(2, gap="large", vertical_alignment="bottom")
    with col1:
        choices = ["nominal", "today"]
        kz.initKey("plots", choices[0])
        ret = kz.getRadio("Dollar amounts in plots", choices, "plots", callback=owb.setDefaultPlots)

    with col2:
        helpmsg = "Click on button if graphs are not all showing."
        st.button(
            "Re-run single case",
            help=helpmsg,
            on_click=owb.runPlan,
            disabled=kz.caseIsNotRunReady(),
        )

    st.divider()
    if kz.isCaseUnsolved():
        st.info("Case status is currently '%s'." % kz.getKey("caseStatus"))
    else:
        owb.plotSingleResults()
