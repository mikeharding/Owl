import streamlit as st


col1, col2, col3, col4 = st.columns(4)
with col4:
    st.image("http://raw.github.com/mdlacasse/owl/main/docs/images/owl.jpg")

st.write('## Owl Retirement Planner')
st.markdown('''
<div style="text-align: justify">

#### A retirement exploration tool based on linear programming

This tool is based on the Owl Python package aimed at providing a retirement modeling
framework for exploring the sensitivity of retirement financial decisions.
Strictly speaking, Owl is not a planning tool, but more an environment for exploring *what if* scenarios.
It provides different realizations of a financial strategy through the rigorous
mathematical optimization of relevant decision variables. Using a linear programming approach,
two major objective goals can be set: either
maximize net spending, or after-tax bequest under various constraints.
Roth conversions are optimized to reduce tax burden, while federal income tax and Medicare
premiums (including IRMAA) are calculated.
See the full description of the package on [github](https://github.com/mdlacasse/owl) for details.

--------------------------------------------------------------------------------------
## Getting started with the user interface
The function of each tab is described in the same order below.
Typically, tabs would be accessed in order, starting from the top.
The `Select case` selection box at the bottom of the margin allows to select an existing case
or create a new one from scratch or from a *case* file, which
contains all the values for the parameters.
This box is present in all relevant tabs and allows to compare different scenarios.

### :orange[Case Setup]
This section contains the steps for creating and configuring case scenarios.

#### Basic Info
This tab controls the creation of scenarios as the `Select case` menu contains
two additional items: one to create a new case, and the other to create a case from a *case* file.
This tab also allows you to duplicate and/or rename a scenario, and to delete scenarios.

For creating a scenario, the (first) name(s), marital status, birth year(s),
and life expectancies are required. A starting date for the plan determines when the plan
starts in the first year. Plan still ends at the end of the year when all individuals
have passed according to the specified life expectancies.

When duplicating a scenario, all parameters will be copied, but each tab in
the `Case setup` section will need to be revisited in order
to refresh the case. This includes the wages and contributions file which will need to
be uploaded.

##### Initializing the life parameters for the realization
Start with the `Select case` box and choose one of `New case...` or `Load case file...`.

If `Load case file...` is selected, a *case* file must be uploaded.
These files end with the *.toml* extension, are human readable (and therefore editable),
and contain all the parameters required to characterize a scenario.
An example is provided
[here](https://raw.github.com/mdlacasse/Owl/main/examples/case_jack+jill.toml) and more
can be found in this [directory](https://github.com/mdlacasse/Owl/blob/main/examples/).
Using a *case* file
will populate all the fields required to run a scenario. A *case* file for the case being developed
can be saved under the [Case Results](#case-results) tab and made available to reload at a later time.
Case files can have any name but when saving from the interface, their name will start with *case_*
followed by the case name.

When starting from `New case...`,
one must provide the year of birth of each spouse(s) and their expected lifespan(s).
For selecting your own numbers, there are plenty of longevity predictors on the web. Pick your favorite:
- [longevityillustrator](https://longevityillustrator.org),
- [livingto100](https://www.livingto100.com/calculator),
- [sunlife](https://www.sunlife.ca/en/tools-and-resources/tools-and-calculators/life-expectancy-calculator/),

or just Google *life expectancy calculator*.

Finally, a start date for the first year or the plan must be provided.
By default, it starts today, but any other date
in the current year can be chosen. This is useful if your numbers are known for a fixed date, or
for reproducibility purposes. This date does not affect when the plan will end, which is at the
end of the year when all inidivuals have passed according to the life parameters data provided.

#### Assets
This tab allows to enter account balances in all savings accounts.
Notice that all amounts are entered in units of \\$1,000, referred to as (\\$k).

Three types of saving accounts are considered and are tracked separately for spouses:
- Taxable saving accounts
- Tax-deferred saving accounts
- Tax-exempt saving accounts


For married couples, the spousal `Beneficiary fractions` associated with these accounts
can be selected, as well as a surplus deposit fraction. The first one controls
how much is left to the surviving spouse while the second determines
how to split potential surplus budget moneys between the taxable accounts of the spouses.
When the `Beneficiary fractions` are not all 1, it is recommended to deposit all
surplus moneys in the taxable account of the first individual to pass. Otherwise,
the optimizer will find creative solutions that can generate surpluses in order
to maximize the final bequest.

#### Wages and Contributions
This tab allows to enter an optional Excel file containing wages and contributions.
This file must contains 9 columns titled as follows:

<span style="font-size: 10px;">

|year|anticipated wages|ctrb taxable|ctrb 401k|ctrb Roth 401k|ctrb IRA|ctrb Roth IRA|Roth X|big-ticket items|
|--|--|--|--|--|--|--|--|--|
|2025 | | | | | | | | |
|2026 | | | | | | | | |
| ... | | | | | | | | |
|20XX | | | | | | | | |

</span>

Here, 20XX is the last row which could be the last year based on the life expectancy values provided.
Missing years or empty cells will be filled with zero values.
For the columns, *anticipated wages* is the annual amount
(gross minus tax-deferred contributions) that you anticipate to receive from employment or other sources
(not including dividends from your taxable investment accounts). Note that column names are case sensitive
and all entries must be in lower case. Best way to start this process is to use the template
file provided [here](https://raw.github.com/mdlacasse/Owl/main/examples/template.xlsx).

For the purpose of planning, there is no clear definition of retirement age. There will be a year,
however, from which you will stop having anticipated income, or diminished income due to decreasing your
work load. This transition can be gradual or sudden, and can be explored through this wages
and contributions file.

Contributions to your savings accounts are marked as *ctrb*. We use 401k as a term which includes
contributions to 403b as well or any other tax-deferred account, with the exception
of IRAs accounts which are treated separately. Contributions to your 401k/403b must
also include your employer's
contributions, if any. As this file is in Excel, one can use the native calculator to enter a percentage
of the anticipated wages for contributions as this can sometimes be easier. Considering a specific example,
assume that Jack earns 100k\\$ and contributes 5% to his 401k which his employer matches at up to 4%,
then Jack's anticipated wages will be (1-.05)*100000 = 95000 and his 401k contributions will be
.09/(1 - .05) * 95000 = 9000. The reason for using 95000 in the last equation allows for making
cross-reference between the cells, as the number 100k\\$ will not appear directly.
Another approach could be to use an additional column with for the total salary and derive numbers
from there. Additional columns on the right can be used for calculations and will be ignored
when the file is read.

Roth conversion can be specified in the column marked *Roth X*. Roth conversion can be advantageous
when performed during the years when the income is lower (and therefore lower tax rates),
typically in the bridge years
between having a full-time regular salary and collecting social security. This column is provided
to override the Roth conversion optimization in Owl. When the option
`Convert as in contribution file` is toggled in the [Optimization Parameters](#optimization-parameters) tab,
values from the contributions file will be used and no optimization over Roth conversions
will be performed. This column is provided for flexibility and to allow comparisons
between an optimized solution and your best guesses.

Finally, *big-ticket items* are used for accounting for the sale or purchase of a house, or any
other major expense or money that you would give or receive (e.g., inheritance, or large gifts
to or from you). Therefore, the sign (+/-) of entries in this column is important.
Positive numbers will be considered in the cash flow for that year and the surplus, if any, will be
deposited in the taxable savings accounts. Negative numbers will potentially generate additional
withdrawals and distributions from retirement accounts. This is the only column that can contain
negative numbers: all other column entries should be positive.

The tab name for each spreadsheet represents the name of the spouse for reporting yearly transactions
affecting the plan. There has to be one tab for each individual and bearing the same name.
Therefore, when running your own case, you will need to rename the tabs in the template file to
have the same names as those used to create the plan
(i.e., *Jack* and *Jill* in the example files provided).

#### Fixed Income
This tab is for entering anticipated fixed income from pensions and social security.
Amounts are in \\$k at the starting date.

#### Rate Selection
This tab allows you to select the return rates over the
time span of the plan. There are two major types of rates:
- *Fixed rates* - staying fixed from one year to another
    - *conversative*
    - *optimistic*
    - *historical average* - i.e., average over a range of past years
    - *user* - rates are provided by the user
- *Varying rates* - varying from year to year
    - *historical* - using a rate sequence which happened in the past
    - *histochastic* - using stochastic rates derived from statistics of historical rates
    - *stochastic* - using stochastic rates created from statistical parameters specified by the user.

These rates are the rates of return for the assets considered. The types of asset are described
in the next section.

#### Asset Allocations
This tab allows you to select how to partition your assets between 4 investment options:
- S&P 500
- Corporate Bonds Baa
- 10-year Treasury Notes
- Cash assets assumed to follow inflation.

Two choices of asset allocations are possible:
*account* and *individual*. For *account* type, each type
of savings account is associated with its own asset allocation ratios.
For *individual*, it is assumed that all savings accounts of a given
individual follow the same allocation ratios, which can vary over the
duration of the plan. It is assumed that the accounts are regularly
rebalanced to maintain the prescribed allocation ratios.

Asset allocations are requested at the beginning and the end of a plan, and
a gliding function (either linear or an s-curve) allows you to glide from the
initial value to the final value as the plan progresses in time.
When an *s-curve* is selected, two additional parameters controlling the curve
will appear, one for the timing of the inflexion point measured in years from now,
and the other for the width of the transition, measured in +/- years from the center.

### Optimization Parameters
This tab allows you to select the optimization parameters.
One can choose between maximizing the net spending amount, or maximizing a bequest.
As one of the two choices is selected as the objective function to optimize, the other becomes
a constraint to obey.

Maximum amount for Roth conversions and who can execute them also needs to be
specified. If a contribution file has been uploaded and the `Convert from contributions file`
is toggled, Roth conversions will not be optimized, but will rather be performed according to
the column `RothX` of the
[Wages and Contributions](#wages-and-contributions).

Calculations of Medicare and IRMAA can be turned on or off. This will typically speed up
the calculations by a factor of 2 to 3, which can be useful when running Monte Carlo simulations.

The time profile of the net spending amount
can be selected to either be flat or follow a *smile* shape.
The smile shape has two configurable parameters: a *dip* percentage
and a linear *increase* over the years (apart from inflation).
Values default to 15% and 12% respectively, but they are configurable
for experimentation.

For married couples, a survivor's
net spending percentage is also configurable. A value of 60% is typically used.
The selected profile curve multiplies
the net spending *basis* which sets the resulting spending
amounts over the duration of the plan.
Notice that *smile* curves are re-scaled to have the same total spending as flat curves:
for that reason they do not start at 1.


--------------------------------------------------------------------------------------
### :orange[Single Scenarios]

#### Case Results
Run a single scenario based on the selections made in the [Case Setup](#case-setup) section.
This simulation runs over a single instance of a series of rates, either fixed or varying.
The outcome is optimized according to the chosen parameters: either maximize the
net spending, of maximize the bequest under the constrait of a net spending amount.
If `Convert from contributions file` is not toggled on,
Roth conversions are optimized for maximizing the selected objective function.
Various plots show the results, which can be displayed in today's \\$ or
in nominal value.

Under this tab, one can also save all the parameters used to generate the
outcome in a *case* file that can be uploaded in the future.

#### Case Worksheets
This tab shows the various worksheets containing annual transactions.
They can be downloaded as an Excel file which looks better than the web representation.

#### Case Summary
This tab shows a summary of the scenario which was computed.
It diplays informative sums of relevant income and spending values.

--------------------------------------------------------------------------------------
### :orange[Multiple Scenarios]

#### Historical Range
This tab allows the user to run multiple similations over a range of historical time spans.
Each simulation assumes that the rates followed a sequence which happened in the past,
starting from each year in the past, and then offset by one year, and so on.
A histogram of results and a success rate is displayed at the end of the run.
$N$ is the number of runs, $P$ the probability of success,
$\\bar{x}$ is the resulting average, and $M$ is the median.

If the `Beneficiary fractions` are not all unity, two histograms will be displayed.

#### Monte Carlo
This tab runs a Monte Carlo simulation using time sequences of return that are generated
statistically using the parameters provided by the user. At the end of the run,
a histogram is shown, with a probability of success.

The mean outcome $\\bar{x}$ and the median $M$ are provided in the graph, as are the number
of cases $N$ and the probability of success $P$, which is the percentage of cases that succeeded.

If the `Beneficiary fractions` are not all unity, two histograms will be displayed.

--------------------------------------------------------------------------------------
### :orange[Resources]
#### Documentation
These pages...

#### Logs
The messages coming from the undelying Owl calculation engine.

#### About Owl
Credits and disclaimers.

''', unsafe_allow_html=True)
