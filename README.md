# sawmill

Simple, beautiful, powerful data analysis and reporting for your logs.

## Motivation

As a member of support, we have to read lots of logs manually that themselves are not structured ...

This means 100ks of logs per week, with an average conservative cost of at least 20 mins spent per case finding the data we need from the logs to help customers. The logs also contain at least 2-3 different contexts or different kinds of logs. 

What about using Datadog or a monitoring tool? 
Sure, that would be great, but now I need to teach an entire team to learn BOTH all of the infrastructure needed to use it, give them authenticated access, make sure the internet isn't down, and teach them a non-standard querying language ... among other things (sadness)

Right now according to metabase, we spend 9.5 days per ticket towards resolution ([source](https://airbyte.metabaseapp.com/dashboard/1590-support-ticket-metrics?date_filter=past3months~&zendesk_only=true&ticket_type=Airbyte%20Cloud%20Support%20Request%20Form&ticket_type=Helpdesk%20From&ticket_type=Self%20Managed%20Enterprise%20Support%20Request%20Form))\

Wouldn't it be nice if we could ask our log questions?
Wouldn't it be even _better_ if we could only look at the lines that are important to us, and reduce the problem space?

### Challenge

How can I get to the truth of the issue from log files in a time-efficient, error-free, reproducible way?
How can I do this without adding complexity to my workflow or the scaling of this process to our entire support/eng teams?

### Implementation

Provide a `sawmill` terminal tool that can take a local file path and SQL script/string command and immediately reduce the results to only the lines that are relevant to me.

### Benefits

- Saves lots of time
- Extensibiliy 
    - The workflow encourages and supports automating itself
    - We can extend this to handle _any_ log or stack trace formatting
- Applicable across multiple teams
- Approachable for our customers 
    - (we can put this tool in their hands someday!)
- Competitive
    - we can maintain rules and optimizations special to our use cases as a company
- Easy to install and learn
- Uses the ubiquity of SQL
- Reduces the number of lines, making issues easier to share, search, and communicate
- This prepares us for larger log datasets, which are inevitable as our customers' use cases grow

## Setup

### Users

1. Install pipx
2. Use pipx to install `sawmill`
```sh
pipx install sawmill
```
3. The user is ready to call `sawmill` from the command line!

4. See [Usage](#usage)

### Developers

1. Install the [pnpm package manager](https://pnpm.io/installation)
2. The development environment assumes [Visual Studio Code](https://code.visualstudio.com/download) as the default project code editor, with the following plugins:
    - Required: 
        - [Markdown Preview Mermaid Support](https://marketplace.visualstudio.com/items?itemName=bierner.markdown-mermaid)
    - Recommended: 
        - [Mermaid Chart](https://marketplace.visualstudio.com/items?itemName=MermaidChart.vscode-mermaid-chart) (free to sign up for an account?)
3. Clone the repository
```sh
# if the user has ssh access to GitHub
git clone git@github.com:bengineerdavis/sawmill.git
```

for everyone else ...

```sh
git clone https://github.com/bengineerdavis/sawmill.git
```
4. Install [`pipx`](https://github.com/pypa/pipx?tab=readme-ov-file#install-pipx)
5. Use `pipx` to install `poetry`
```sh
pipx install poetry
```
6. OPTIONAL: the user may set up their own `virtual environment` or let `poetry` to manage it for them
7. Navigate into the new local `sawmill` directory
```sh
cd sawmill
```
8. Use pipx to make an editable installation of sawmill on the user's local machine
```sh
pipx install -e .
```
9. Install project dependencies 
```sh
make install
``` 
10. Ready to contribute!

## Usage

```bash
# command returns pandas DataFrame with user-select columns and rows defined in the SQL script

sawmill [path/to/file] [sql command string]|[sql command from file.sql]

