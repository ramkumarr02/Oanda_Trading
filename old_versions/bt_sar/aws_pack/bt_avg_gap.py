from utils.packages import *
from utils.variables import *
from utils.i_o import *
from utils.dir_slope import *
from utils.engine import *
from utils.loops import *
from utils.order import *
# import winsound


data = run_engine(data)
generate_result_report(data)
plot_graph(data)

