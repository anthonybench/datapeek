from os import getenv, path
from yaml import safe_load

# environment
home_dir = getenv('HOME')

supported_formats = {
  'csv':'data',
  'json': 'data',
  'parquet': 'data',
  'pkl': 'data',
  'xlsx': 'data',
  'pdf': 'metadata',
  'png': 'metadata',
  'jpg': 'metadata',
  'jpeg': 'metadata',
}
sample_data_table_type = 'simple'

#───CONFIG FILE──────────────
global_config_path = f'{home_dir}/.sleepyconfig/params.yml'
config_file_exists = path.exists(global_config_path)

def resolveValue(default:any, config_key:str) -> any:
  '''returns config value if exists, else default'''
  if not config_file_exists:
    return default
  with open(global_config_path, 'r') as f:
    raw_config = safe_load(f)
    if config_key not in raw_config:
      return default
    return raw_config[config_key]
  
## defaults
default_table_style = 'rounded_grid'
default_sample_output_limit = 5
default_max_terminal_width = 80
## config file
datapeek_table_style = resolveValue(default_table_style, 'datapeek_table_style')
sample_output_limit = resolveValue(default_sample_output_limit, 'datapeek_sample_size')
set_max_terminal_width = resolveValue(default_max_terminal_width, 'datapeek_max_terminal_width')