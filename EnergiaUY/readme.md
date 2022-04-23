# EnergiaUY - Python

Function triggered for the hourly tweet, with the information of the energy origins for Uruguay.

## How it works

For a `TimerTrigger` to work, you provide a schedule in the form of a [cron expression](https://en.wikipedia.org/wiki/Cron#CRON_expression). In this case executes every `0 *:30 * * * *` or each hour at the 30mins mark and gets the information from UTE's public site.


<TODO> Documentation
