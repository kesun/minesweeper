from pyramid.view import view_config, view_defaults
from minesweeper.grid import Grid

g_grid = None

## modify the game to your liking
## BASIC RULE OF THUMB: MINE_COUNT <= GRID_WIDTH * GRID_HEIGHT
GRID_WIDTH = 10
GRID_HEIGHT = 8
MINE_COUNT = 5

@view_defaults(renderer='templates/minesweeper.pt')
class MineSweeperViews:
	def __init__(self, request):
		self.request = request

	@view_config(route_name='newgrid', request_method='GET')
	@view_config(route_name='newgrid_json', renderer='json')
	def StartGame(request):
		print("StartGame requested")
		global g_grid
		global GRID_HEIGHT
		global GRID_WIDTH
		global MINE_COUNT
		if g_grid == None:
			g_grid = Grid(GRID_WIDTH, GRID_HEIGHT, MINE_COUNT)
		return {'field': g_grid.field, 'state': g_grid.state}

	@view_config(route_name='playgrid', request_method="POST")
	@view_config(route_name='playgrid_json', renderer='json')
	def Play(request):
		# print("Play request", request)
		global g_grid
		global GRID_HEIGHT
		global GRID_WIDTH
		global MINE_COUNT
		event = request.request.json.get('event')

		if event == "leftClick" or event == "rightClick":
			x = request.request.json.get('x')
			y = request.request.json.get('y')
			g_grid.pokeCell(x, y, event)
			#print("Play request got data", event, x, y)
		elif event == "restart":
			g_grid = Grid(GRID_WIDTH, GRID_HEIGHT, MINE_COUNT)

		# make getters for .field and .state
		return {'field': g_grid.field, 'state': g_grid.state}
