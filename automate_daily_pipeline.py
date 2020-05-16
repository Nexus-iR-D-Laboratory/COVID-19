import requests
import git
import sys

import covid_moving_window as cmv

data_url = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv"
print(f'Downloading data from {data_url}')

# download and format data
req = requests.get(data_url)
unformatted_data = req.content.decode('utf-8')
data = [line.split(',') for line in unformatted_data.split('\n')]
header_line = data[0]
data_lines = data[1:]
data_dict = {
    header: list() for header in header_line
}
for line in data_lines:
    for i, header in enumerate(header_line):
        data_dict[header].append(line[i])

# Update covid_moving_window.py to today’s max_date_str
max_date_str = data_dict['date'][-1]
cmv.opt_simplified = True # monkey-patching
cmv.run_everything(max_date_str)

# Re-run generate_plot_browser_moving_window_statsmodels_only.py with the updated hyperparameter string
import generate_plot_browser_moving_window_statsmodels_only

# Push updated plot_browser_moving_window_statsmodels_only directory to GitHub
pbmwso_folder = './plot_browser_moving_window_statsmodels_only/'
repo = None
try:
    repo = git.Repo()
    assert not repo.bare
except:
    print('No .git in current directory. Run again from within git repo you want to update.')
    sys.exit()

try:
    origin = repo.remote(name='origin')
    assert origin.exists()
    origin.fetch()
except:
    print('No valid remote repo found for current branch.')
    sys.exit()

try:
    repo.git.add(pbmwso_folder)
    repo.git.commit(m=f'Update {pbmwso_folder} with data up to date {max_date_str}')
    origin.push()
except:
    print(f'Error when attempting to upload {pbmwso_folder} to git. Check that data has actually been modified.')
