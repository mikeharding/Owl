import streamlit as st

import sskeys as k
import owlbridge as owb


profileChoices = ['smile', 'flat']
k.init('profile', profileChoices[0])
k.init('survivor', 60)


def initProfile():
    owb.setProfile(profileChoices[0], False)


k.runOncePerCase(initProfile)

ret = k.titleBar('opto')
st.write('## Optimization Parameters')

if ret is None:
    st.info('Case(s) must be first created before running this page.')
else:
    col1, col2 = st.columns(2, gap='large', vertical_alignment='top')
    with col1:
        choices = ['Net spending', 'Bequest']
        helpmsg = "Value is in today's $"
        k.init('objective', choices[0])
        ret = k.getRadio("Maximize", choices, 'objective')

    with col2:
        if k.getKey('objective') == 'Net spending':
            k.init('bequest', 0)
            ret = k.getNum("Desired bequest ($k)", 'bequest', help=helpmsg)

        else:
            k.init('netSpending', 0)
            ret = k.getNum("Desired annual net spending ($k)", 'netSpending', help=helpmsg)

    st.divider()
    col1, col2 = st.columns(2, gap='large', vertical_alignment='top')
    with col1:
        iname0 = k.getKey('iname0')
        helpmsg = "Value is in nominal $"
        k.init('readRothX', False)
        fromFile = k.getKey('readRothX')
        k.init('maxRothConversion', 50)
        ret = k.getNum("Maximum Roth conversion ($k)", 'maxRothConversion', disabled=fromFile, help=helpmsg)
        ret = k.getToggle('Convert as in contributions file', 'readRothX')

    with col2:
        if k.getKey('status') == 'married':
            iname1 = k.getKey('iname1')
            choices = ['None', iname0, iname1]
            k.init('noRothConversions', choices[0])
            helpmsg = "`None` means no exclusion. Set `Maximum Roth conversion` to 0 to exclude both spouses."
            ret = k.getRadio("Exclude Roth conversions for...", choices,
                             "noRothConversions", help=helpmsg)

    st.divider()
    k.init('withMedicare', True)
    col1, col2 = st.columns(2, gap='large', vertical_alignment='top')
    with col1:
        ret = k.getToggle('Medicare and IRMAA calculations', 'withMedicare')
    with col2:
        if owb.hasMOSEK():
            choices = ['HiGHS', 'MOSEK']
            k.init('solver', choices[0])
            ret = k.getRadio('Solver', choices, 'solver')

    st.divider()
    col1, col2 = st.columns(2, gap='large', vertical_alignment='top')
    with col1:
        ret = k.getRadio("Spending profile", profileChoices, 'profile', callback=owb.setProfile)

    with col2:
        if k.getKey('status') == 'married':
            ret = k.getIntNum("Survivor's spending (%)", 'survivor', callback=owb.setProfile)

    st.divider()
    owb.showProfile()
