"""
Cookie Clicker Simulator
"""

import simpleplot, math

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    
    def __init__(self):
        self._total_cookies = 0.0
        self._current_cookies = 0.0
        self._current_time = 0.0
        self._current_cps = 1.0
        self._history = [(0.0, None, 0.0, 0.0)]
        
    def __str__(self):
        """
        Return human readable state
        """
        state = "Time: " + str(self.get_time()) + "\nCurrent Cookies: " \
        + repr(self.get_cookies()) + "\nCurrent CPS: " + repr(self.get_cps()) \
        + "\nTotal Cookies: " + repr(self._total_cookies) + "\n"
        return state
        
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self._current_cookies
    
    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._current_cps
    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._current_time
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: [(0.0, None, 0.0, 0.0)]

        Should return a copy of any internal data structures,
        so that they will not be modified outside of the class.
        """
        return self._history

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0.0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        if self._current_cookies >= cookies :
            return 0.0
        else :
            return math.ceil((cookies - self._current_cookies) / 
                             self._current_cps)
    
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0.0
        """
        if time > 0.0 :
            cookie_update = self._current_cps * time
            self._current_time += time
            self._current_cookies += cookie_update
            self._total_cookies += cookie_update
    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if self._current_cookies >= cost :
            self._current_cookies -= cost
            self._current_cps += additional_cps
            self._history.append((self._current_time, item_name, 
                                  cost, self._total_cookies))
            #print [self._current_time, item_name, cost, self._total_cookies]
   
    
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.
    """
    info = build_info.clone()
    clicker = ClickerState()
    while duration >= 0 :
        item = strategy(clicker.get_cookies(), clicker.get_cps(), 
                        clicker.get_history(), duration, info)
        
        if item is None :
            break
            
        cost = info.get_cost(item)
        wait_time = clicker.time_until(cost)
        
        if wait_time > duration :
            break
        
        clicker.wait(wait_time)
        clicker.buy_item(item, cost, info.get_cps(item))
        duration -= wait_time
        info.update_item(item)
        
    clicker.wait(duration)
        
    return clicker


def strategy_cursor_broken(cookies, cps, history, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic (and broken) strategy does not properly
    check whether it can actually buy a Cursor in the time left.  Your
    simulate_clicker function must be able to deal with such broken
    strategies.  Further, your strategy functions must correctly check
    if you can buy the item in the time left and return None if you
    can't.
    """
    return "Cursor"

def strategy_none(cookies, cps, history, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that will never buy anything, but
    that you can use to help debug your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, history, time_left, build_info):
    """
    Always buy the cheapest item you can afford in the time left.
    """
    items = build_info.build_items()
    items_costs = map(build_info.get_cost, items)
    cheap_idx = items_costs.index(min(items_costs))
    name = items[cheap_idx]
    if (cookies + cps * time_left) < items_costs[cheap_idx] :
        name = None
    return name

def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
    items = build_info.build_items()
    item_cost = 0.0
    name = None
    for item in items :
        cost = build_info.get_cost(item)
        if item_cost < cost <= (cookies + cps * time_left) :
            item_cost = cost
            name = item
    return name

def strategy_best(cookies, cps, history, time_left, build_info):
    """
    The best strategy that you are able to implement.
    """
    items = build_info.build_items()
    items_costs = map(build_info.get_cost, items)
    items_cps = map(build_info.get_cps, items)
    items_costs_per_cps = tuple(map(lambda x, y: float(x) / y, items_costs, items_cps))
    idx = items_costs_per_cps.index(min(items_costs_per_cps))
    name = items[idx]
    if (cookies + cps * time_left) < items_costs[idx] :
        name = None
    return name

def strategy_best2(cookies, cps, history, time_left, build_info):
    """
    The best strategy that you are able to implement.
    """
    items = build_info.build_items()
    item_cost = 0.0
    name = None
    for item in items :
        cost = build_info.get_cost(item)
        if item_cost < cost <= (cookies + cps * time_left) / 20 :
            item_cost = cost
            name = item
    return name

def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation for the given time with one strategy.
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    # history = state.get_history()
    # history = [(item[0], item[3]) for item in history]
    # simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """    
    run_strategy("Cursor", SIM_TIME, strategy_cursor_broken)

    # Add calls to run_strategy to run additional strategies
    run_strategy("Cheap", SIM_TIME, strategy_cheap)
    run_strategy("Expensive", SIM_TIME, strategy_expensive)
    run_strategy("Best", SIM_TIME, strategy_best)
    run_strategy("Best2", SIM_TIME, strategy_best2)
    
run()