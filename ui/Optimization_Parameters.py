import streamlit as st

import sskeys as kz
import owlbridge as owb


profileChoices = ["flat", "smile"]
kz.initKey("spendingProfile", profileChoices[1])
kz.initKey("survivor", 60)
kz.initKey("smileDip", 15)
kz.initKey("smileIncrease", 12)
kz.initKey("smileDelay", 0)


def initProfile():
    owb.setProfile(profileChoices[0], False)


ret = kz.titleBar("Optimization Parameters")

if ret is None or kz.caseHasNoPlan():
    st.info("Case(s) must be first created before running this page.")
else:
    kz.runOncePerCase(initProfile)

    st.write("##### Objective")
    col1, col2 = st.columns(2, gap="large", vertical_alignment="top")
    with col1:
        choices = ["Net spending", "Bequest"]
        helpmsg = "Value is in today's \\$k."
        kz.initKey("objective", choices[0])
        ret = kz.getRadio("Maximize", choices, "objective")

    with col2:
        if kz.getKey("objective") == "Net spending":
            kz.initKey("bequest", 0)
            ret = kz.getNum("Desired bequest (\\$k)", "bequest", help=helpmsg)

        else:
            kz.initKey("netSpending", 0)
            ret = kz.getNum("Desired annual net spending (\\$k)", "netSpending", help=helpmsg)

    st.divider()
    st.write("##### Roth Conversions")
    col1, col2 = st.columns(2, gap="large", vertical_alignment="top")
    with col1:
        iname0 = kz.getKey("iname0")
        helpmsg = "Value is in nominal \\$k."
        kz.initKey("readRothX", False)
        fromFile = kz.getKey("readRothX")
        kz.initKey("maxRothConversion", 50)
        ret = kz.getNum("Maximum Roth conversion (\\$k)", "maxRothConversion", disabled=fromFile, help=helpmsg)
        ret = kz.getToggle("Convert as in wages and contributions tables", "readRothX")

    with col2:
        if kz.getKey("status") == "married":
            iname1 = kz.getKey("iname1")
            choices = ["None", iname0, iname1]
            kz.initKey("noRothConversions", choices[0])
            helpmsg = "`None` means no exclusion. Set `Maximum Roth conversion` to 0 to exclude both spouses."
            ret = kz.getRadio("Exclude Roth conversions for...", choices, "noRothConversions", help=helpmsg)

    st.divider()
    st.write("##### Medicare")
    kz.initKey("withMedicare", True)
    col1, col2 = st.columns(2, gap="large", vertical_alignment="top")
    with col1:
        helpmsg = "Do or do not perform additional Medicare and IRMAA calculations."
        ret = kz.getToggle("Medicare and IRMAA calculations", "withMedicare", help=helpmsg)
    with col2:
        if kz.getKey("withMedicare"):
            helpmsg = "MAGI in nominal $k for that previous year."
            years = owb.backYearsMAGI()
            for ii in range(2):
                kz.initKey("MAGI" + str(ii), 0)
                if years[ii] > 0:
                    ret = kz.getNum(f"MAGI for year {years[ii]} ($k)", "MAGI" + str(ii), help=helpmsg)

    if owb.hasMOSEK():
        st.divider()
        st.write("##### Solver")
        choices = ["HiGHS", "MOSEK"]
        kz.initKey("solver", choices[0])
        ret = kz.getRadio("Linear programming solver", choices, "solver")

    st.divider()
    st.write("##### Spending Profile")
    col1, col2, col3 = st.columns(3, gap="medium", vertical_alignment="top")
    with col1:
        ret = kz.getRadio("Type of profile", profileChoices, "spendingProfile", callback=owb.setProfile)
    with col2:
        if kz.getKey("status") == "married":
            helpmsg = "Percentage of spending required for the surviving spouse."
            ret = kz.getIntNum(
                "Survivor's spending (%)", "survivor", max_value=100, help=helpmsg, callback=owb.setProfile
            )
        if kz.getKey("spendingProfile") == "smile":
            helpmsg = "Time in year before spending starts decreasing."
            ret = kz.getIntNum(
                "Smile delay (in years from now)", "smileDelay", max_value=30, help=helpmsg, callback=owb.setProfile
            )
            with col3:
                helpmsg = "Percentage to decrease for the slow-go years."
                ret = kz.getIntNum("Smile dip (%)", "smileDip", max_value=100, help=helpmsg, callback=owb.setProfile)
                helpmsg = "Percentage to increase (or decrease) over time period."
                ret = kz.getIntNum(
                    "Smile increase (%)",
                    "smileIncrease",
                    min_value=-100,
                    max_value=100,
                    help=helpmsg,
                    callback=owb.setProfile,
                )

    st.divider()
    col1, col2 = st.columns(2, gap="small")
    with col1:
        st.write("##### Spending Profile")
        owb.showProfile()
