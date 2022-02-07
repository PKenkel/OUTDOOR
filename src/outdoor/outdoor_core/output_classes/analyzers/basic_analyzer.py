#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 26 15:12:24 2022

@author: philippkenkel
"""

import os
import pickle5 as pic5
import time
import copy
from tabulate import tabulate
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime
import pydot
import sys


class BasicModelAnalyzer:
    def __init__(self, model_output=None):

        self.model_output = copy.deepcopy(model_output)

# -----------------------------------------------------------------------------
# -------------------------Private methods ------------------------------------
# -----------------------------------------------------------------------------

    def _collect_capitalcost_shares(self, model_data):
        """
        Decription
        ----------
        Collects data from the ProcessResults._data dictionary.
        Data that is collected are the shares (in %) of different unit-operations
        in the total annual capital investment. Data is returned as dictionary

        Returns
        -------
        capitalcost_shares : Dictionary

        """
        capitalcost_shares = {"Capital costs shares": {}}

        total_costs = model_data["CAPEX"]

        capitalcost_shares["Capital costs shares"]["Heat pump"] = round(
            model_data.get("ACC_HP", 0) / total_costs * 100, 2
        )

        for i, j in model_data["ACC"].items():
            if j >= 1e-3:
                index_name = model_data["Names"][i]
                capitalcost_shares["Capital costs shares"][index_name] = round(
                    (j + model_data.get("TO_CAPEX", 0).get(i, 0)) / total_costs * 100, 2
                )

        return capitalcost_shares

    def _collect_economic_results(self, model_data):
        """
        Description
        -----------
        Collects data from the ProcessResults._data dictionary.
        Data that is collected are base economic values, and depict the shares
        of the total costs of:
            CAPEX (all unit-operations)
            Raw material purchase
            Electricity costs
            Chilling costs
            Heat integration costs (Heating, Cooling utilities as well as HEN)
            Operating and Maintenance
            Waste water treatment
            Profits from Byproducts

        Returns
        -------
        economic_results : Dictionary

        """
        economic_results = {"Economic results": {}}

        total_costs = model_data["TAC"] / 1000

        profits = 0
        wwt = 0

        for i, j in model_data["PROFITS"].items():
            if j < 0:
                wwt -= j * model_data["H"] / 1000
            else:
                profits -= j * model_data["H"] / 1000

        economic_results["Economic results"]["CAPEX share"] = round(
            model_data.get("CAPEX", 0) / total_costs * 100, 2
        )

        economic_results["Economic results"]["Raw material consumption share"] = round(
            model_data.get("RM_COST_TOT", 0) / 1000 / total_costs * 100, 2
        )

        economic_results["Economic results"]["Operating and Maintanence share"] = round(
            model_data.get("M_COST_TOT", 0) / total_costs * 100, 2
        )

        economic_results["Economic results"]["Electricity share"] = round(
            (
                model_data.get("ENERGY_COST", 0).get("Electricity", 0)
                + model_data.get("ELCOST", 0)
            )
            / 1000
            / total_costs
            * 100,
            2,
        )

        economic_results["Economic results"]["Chilling share"] = round(
            model_data.get("ENERGY_COST", 0).get("Chilling", 0)
            / 1000
            / total_costs
            * 100,
            2,
        )

        economic_results["Economic results"]["Heat integration share"] = round(
            model_data.get("C_TOT", 0) / 1000 / total_costs * 100, 2
        )

        economic_results["Economic results"]["Waste treatment share"] = round(
            wwt / total_costs * 100, 2
        )

        economic_results["Economic results"]["Profits share"] = round(
            profits / total_costs * 100, 2
        )

        return economic_results

    def _collect_electricity_shares(self, model_data):
        """
        Description
        -----------
        Collects data from the ProcessResults._data dictionary.
        Data that is collected are the shares (in %) of different unit-operations
        in the total electricity demand.

        Returns
        -------
        electricity_shares : Dictionary


        """
        electricity_shares = {"Electricity demand shares": {}}

        total_el = model_data.get("ENERGY_DEMAND_HP_EL", 0) * model_data["H"]

        for i, j in model_data["ENERGY_DEMAND"].items():
            if i[1] == "Electricity" and j >= 1e-05:
                total_el += j * model_data.get("flh", 0).get(i[0], 0)

        electricity_shares["Electricity demand shares"][
            "Heatpump electricity share"
        ] = round(
            model_data.get("ENERGY_DEMAND_HP_EL", 0) * model_data["H"] / total_el * 100,
            2,
        )

        for i, j in model_data["ENERGY_DEMAND"].items():
            if i[1] == "Electricity" and j >= 1e-05:
                index_name = model_data["Names"][i[0]]
                electricity_shares["Electricity demand shares"][index_name] = round(
                    j * model_data.get("flh", 0).get(i[0], 0) / total_el * 100, 2
                )

        return electricity_shares

    def _collect_heatintegration_results(self, model_data):
        """
        Description
        -----------

        Collects data from the ProcessResults._data dictionary.
        Data that is collected are basic heat integration data:
            Total heating / cooling demand (in MW)
            Total heat recovery (from unit-operations) (in MW)
            Total High pressure steam production, internal (in MW)
            Total internal usage of this HP steam (rest is sold to market)
            Total Heat supplied by High Temperature heat pump (in MW)
            Net heating and cooling demand (in MW)

        Returns
        -------
        heatintegration_results : Dictionary


        """
        heatintegration_results = {"Heating and cooling": {}}

        total_heating = 0
        total_cooling = 0
        net_heating = 0
        steam = 0

        for i in model_data["ENERGY_DEMAND_HEAT_UNIT"].values():
            if i >= 1e-05:
                total_heating += i

        for i in model_data["ENERGY_DEMAND_COOL_UNIT"].values():
            if i >= 1e-05:
                total_cooling += i

        for i in model_data["ENERGY_DEMAND_HEAT_PROD"].values():
            if i >= 1e-05:
                steam += i

        for i in model_data["ENERGY_DEMAND_HEAT_DEFI"].values():
            if i >= 1e-05:
                net_heating += i

        heatintegration_results["Heating and cooling"]["Total heating demand"] = round(
            total_heating, 2
        )

        heatintegration_results["Heating and cooling"]["Total cooling demand"] = round(
            total_cooling, 2
        )

        heatintegration_results["Heating and cooling"]["Total heat recovery"] = round(
            model_data["EXCHANGE_TOT"], 2
        )

        heatintegration_results["Heating and cooling"]["HP Steam produced"] = round(
            steam, 2
        )

        heatintegration_results["Heating and cooling"][
            "Internally used HP Steam"
        ] = round(model_data.get("ENERGY_DEMAND_HEAT_PROD_USE", 0), 2)

        heatintegration_results["Heating and cooling"][
            "High temperature heat pump heat supply"
        ] = round(model_data.get("ENERGY_DEMAND_HP_USE", 0), 2)

        heatintegration_results["Heating and cooling"]["Net heating demand"] = round(
            net_heating, 2
        )

        heatintegration_results["Heating and cooling"]["Net cooling demand"] = round(
            model_data.get("ENERGY_DEMAND_COOLING", 0), 2
        )

        return heatintegration_results

    def _collect_GHG_results(self, model_data):
        """
        Description
        -----------
        Collects data from the ProcessResults._data dictionary.
        Data that is collected are the annual GHG emissions from:
            Direct emissions in unit-operations (sum in t/y)
            Indirect emissions from Electricity and Chilling (sum in t/y)
            Indirect emissions from Heat (sum in t/y)
            Emissions from building the plant (t/y)
            Emissions from buying raw materials / Negative emissions
                from carbon capture (t/y)
            Avoided burden credits from byproduct selling (t/y)

        Returns
        -------
        GHG_results : Dictionary

        """
        GHG_results = {"Green house gas emission shares": {}}

        ghg_d = 0
        ghg_b = 0
        ghg_ab = 0

        for i in model_data["GWP_U"].values():
            if i is not None and i >= 1e-05:
                ghg_d += i

        for i in model_data["GWP_UNITS"].values():
            if i is not None and i >= 1e-05:
                ghg_b += i

        for i in model_data["GWP_CREDITS"].values():
            if i is not None and i >= 1e-05:
                ghg_ab += i

        GHG_results["Green house gas emission shares"]["Direct emissions"] = round(
            ghg_d, 0
        )

        GHG_results["Green house gas emission shares"]["Electricity"] = round(
            model_data.get("GWP_UT", 0).get("Electricity", 0), 0
        )

        GHG_results["Green house gas emission shares"]["Heat"] = round(
            model_data.get("GWP_UT", 0).get("Heat", 0), 0
        )

        GHG_results["Green house gas emission shares"]["Chilling"] = round(
            model_data.get("GWP_UT", 0).get("Chilling", 0), 0
        )

        GHG_results["Green house gas emission shares"][
            "Plant building emissions"
        ] = round(ghg_b, 0)

        GHG_results["Green house gas emission shares"][
            "Raw Materials / Carbon Capture"
        ] = round(-model_data["GWP_CAPTURE"], 0)

        GHG_results["Green house gas emission shares"][
            "Avoided burden for byproducts"
        ] = round(-ghg_ab, 0)

        return GHG_results

    def _collect_FWD_results(self, model_data):
        """
        Description
        -----------
        Collects data from the ProcessResults._data dictionary.
        Data that is collected are the annual fresh water demand from:
            Indirect demand from Electricity and Chilling (sum in t/y)
            Indirect demand from Heat (sum in t/y)
            Demand from buying raw materials
            Avoided burden credits from byproduct selling (t/y)

        Returns
        -------
        FWD_results: Dictionary
        """

        FWD_results = {"Fresh water demand shares": {}}

        FWD_results["Fresh water demand shares"][
            "Indirect demand from raw materials"
        ] = round(-model_data.get("FWD_S", 0), 0)

        FWD_results["Fresh water demand shares"][
            "Utilities (Electricity and chilling)"
        ] = round(model_data.get("FWD_UT1", 0), 0)

        FWD_results["Fresh water demand shares"]["Utilities (Heating)"] = round(
            model_data.get("FWD_UT2", 0), 0
        )

        FWD_results["Fresh water demand shares"][
            "Avoided burden from byproducds"
        ] = round(-model_data.get("FWD_C", 0), 0)

        return FWD_results

    def _collect_energy_data(self, model_data):
        energy_data = {"Energy data": {}}

        heat_demand = model_data["ENERGY_DEMAND_HEAT_UNIT"]
        cool_demand = model_data["ENERGY_DEMAND_COOL_UNIT"]

        total_el = model_data.get("ENERGY_DEMAND_HP_EL", 0) * model_data["H"]

        for i, j in model_data["ENERGY_DEMAND"].items():
            if i[1] == "Electricity" and abs(j) >= 1e-05:
                total_el += j * model_data.get("flh", 0).get(i[0], 0)

        energy_data["Energy data"]["heat"] = heat_demand
        energy_data["Energy data"]["cooling"] = cool_demand
        energy_data["Energy data"]["electricity"] = total_el

        return energy_data

    def _collect_mass_flows(self, model_data):
        mass_flow_data = {"Mass flows": {}}

        for i, j in model_data["FLOW_FT"].items():
            if j > 1e-04:
                mass_flow_data["Mass flows"][i] = round(j, 2)

        for i, j in model_data["FLOW_ADD"].items():
            if j > 1e-04:
                mass_flow_data["Mass flows"][i] = round(j, 2)

        return mass_flow_data

    def _collect_techno_economic_results(self):
        self.results = dict()

        model_data = self.model_output._data

        chosen_technologies = {"Chosen technologies": self.model_output.return_chosen()}
        self.results.update(chosen_technologies)

        self.results.update(self._collect_economic_results(model_data))
        self.results.update(self._collect_capitalcost_shares(model_data))
        self.results.update(self._collect_electricity_shares(model_data))
        self.results.update(self._collect_heatintegration_results(model_data))
        self.results.update(self._collect_energy_data(model_data))

        return self.results

    def _collect_environmental_data(self):

        self.results = dict()
        model_data = self.model_output._data
        self.results.update(self._collect_GHG_results(model_data))
        self.results.update(self._collect_FWD_results(model_data))

        return self.results

    def _print_results(self, data=None):
        """
        Description
        -------
        Collects all important results data and prints them as tables to the
        console.

        """

        all_results = data

        for i, j in all_results.items():
            print("")
            print("")
            print(i)
            print("--------------")
            print(tabulate(j.items()))
            print("")

    def _save_results(self, data, path, suffix=None):
        """

        Parameters
        ----------
        path : String type of where to save the results as .txt file

        Decription
        -------
        Collects all important results from the ProcessResults Class object and
        saves the data as tables in a text file.

        """
        all_results = data

        if not os.path.exists(path):
            os.makedirs(path)

        path = path + suffix + self.model_output._case_time + ".txt"

        with open(path, encoding="utf-8", mode="w") as f:

            for i, j in all_results.items():
                table = tabulate(j.items())

                f.write("\n")
                f.write(i)
                f.write("-------- \n")
                f.write(table)
                f.write("\n")
                f.write("\n \n")

            print("")

    # -----------------------------------------------------------------------------
    # -------------------------Public methods -------------------------------------
    # -----------------------------------------------------------------------------

    def set_model_output(self, model_output):
        """
        Parameters
        ----------
        model_output : MultiModelOutput Class
            Store MultiModelOutput Object in ModelAnalyzer

        """
        self.model_output = copy.deepcopy(model_output)

    def load_model_output(self, path):
        """
        Parameters
        ----------
        path : String
            Path string from where to load pickle file

        """

        timer = time.time()

        with open(path, "rb") as file:
            self.model_output = pic5.load(file)

        timer = time.time() - timer
        print(f"File loading time was {timer} seconds")

    def techno_economic_analysis(self, pprint=True, save=None):

        data = self._collect_techno_economic_results()

        if pprint is True:
            self._print_results(data)

        if save is not None:
            suffix = "/techno_economic_results"
            self._save_results(data=data, path=save, suffix=suffix)

    def environmental_analysis(self, pprint=True, save=None):
        data = self._collect_environmental_data()

        if pprint is True:
            self._print_results(data)

        if save is not None:
            suffix = "/environmental_results"
            self._save_results(data=data, path=save, suffix=suffix)

    def create_plot_bar(self, user_input, save=False, Path=None, gui=False):

        INPUT_SET = {
            "Economic results",
            "Capital costs shares",
            "Fresh water demand shares",
            "Green house gas emission shares",
            "Heating and cooling",
            "Electricity demand shares",
        }
        
        if user_input not in INPUT_SET:
            print('The user input is not correct, please only select from:')
            print(INPUT_SET)
            sys.exit()
            

        fig = plt.figure()
        ax1 = fig.add_subplot()
        dict1 = self._collect_techno_economic_results()
        model_data = self.model_output._data
        dict1.update(self._collect_GHG_results(model_data))
        dict1.update(self._collect_FWD_results(model_data))

        data = dict1[user_input]

        labels = list()
        values = list()

        for i, j in data.items():
            labels.append(i)
            values.append(j)

        value_sum = round(sum(values))

        series = pd.Series(data=data, index=data.keys(), name=" ")

        plot_labels = {
            "Breakdown": None,
            "titel": user_input,
            "total": " ",
        }

        if value_sum == 100:
            plot_labels["Breakdown"] = "Breakdown (%)"

            if user_input == "Economic results":
                NPC = round(model_data["NPC"])
                plot_labels["total"] = f"NPC are {NPC} €/ ton"

        else:
            if user_input == "Heating and cooling":
                plot_labels["Breakdown"] = "Amounts in MW"

            else:
                plot_labels["Breakdown"] = "Breakdown"

        if plot_labels["total"]:
            total = plot_labels["total"]
        else:
            total = None

        titel = plot_labels["titel"]

        plt.rcParams["figure.dpi"] = 160

        my_colors = plt.cm.Greys(np.linspace(0.0, 0.7, len(values)))

        axes = pd.DataFrame(series).T.plot(
            kind="bar",
            stacked=True,
            rot="horizontal",
            figsize=(3, 4),
            title=f" {titel}, {total}",
            edgecolor="k",
            color=my_colors,
            legend=None,
            ax=ax1,
        )

        ax1.tick_params(
            axis="x", which="both", bottom=False, top=False, labelbottom=False
        )

        axes.spines["top"].set_visible(False)

        colLabels = [plot_labels["Breakdown"] for i in range(len(values))]
        array = np.array(values, dtype=float).reshape((len(values), 1))

        ax1.table(
            cellText=array,
            rowLabels=labels,
            rowColours=my_colors,
            colLabels=colLabels,
            cellLoc="center",
            loc="bottom",
        )

        # Save input file if save statement = True
        if save is True:
            date_time_now = datetime.datetime.now().strftime("%Y_%m_%d__%H-%M-%S")

            if Path is None:
                my_path = os.path.abspath(__file__)
                plt.savefig(
                    "/{}_Chart_{}.pdf".format(date_time_now, user_input),
                    dpi=160,
                    bbox_inches="tight",
                )
                print("Saved in {}".format(my_path))

            if Path is not None:
                assert os.path.exists(
                    Path
                ), "This file path does not seem to exist: " + str(Path)
                plt.savefig(
                    Path.rstrip(".py")
                    + "/{}_Chart_{}.pdf".format(date_time_now, user_input),
                    dpi=160,
                    bbox_inches="tight",
                )
                print("Saved in {}".format(Path))

        # Create temp-file for presentation in GUI
        if gui is True:
            plt.savefig("temp/new.png", dpi=160, bbox_inches="tight")

        return fig

    def create_flowsheet(self, path):
        def make_node(graph, name, shape):
            """
            Parameters
            ----------
            graph : Dot class
            name : String

            shape : String (Options check documentation of graphviz module)

            Returns
            -------
            node : Pydot Node object

            """

            node = pydot.Node(name, height=0.5, width=2, fixedsize=True)
            node.set_shape(shape)
            graph.add_node(node)

            return node

        def make_link(graph, a_node, b_node, label=None, width=1, style="solid"):
            """

            Parameters
            ----------
            graph : Dot object
            a_node : pydot node object (starting point)
            b_node : pydot node object (ending point)
            label : Label (can be string but also float etc. )
            width :
                DESCRIPTION. The default is 1.
            style : TYPE, optional
                DESCRIPTION. The default is 'solid'. For options check
                            documentation of graphviz module

            Returns
            -------
            edge : pydot Edge object

            """
            edge = pydot.Edge(a_node, b_node)
            edge.set_penwidth(width)
            edge.set_style(style)

            if label is not None:
                edge.set_label(label)

            graph.add_edge(edge)

            return edge

        data = dict()
        nodes = dict()
        edges = dict()
        model_data = self.model_output._data
        data = self._collect_mass_flows(model_data)["Mass flows"]
        flowchart = pydot.Dot(
            "flowchart", rankdir="LR", ratio="compress", size="15!,1", dpi="500"
        )

        for i, j in data.items():

            for v in i:

                if v not in nodes.keys():

                    if v in model_data["U_S"]:
                        nodes[v] = make_node(
                            flowchart, model_data["Names"][v], "ellipse"
                        )

                    elif v in model_data["U_STOICH_REACTOR"]:

                        if v in model_data["U_TUR"]:
                            nodes[v] = make_node(
                                flowchart, model_data["Names"][v], "doubleoctagon"
                            )

                        elif v in model_data["U_FUR"]:
                            nodes[v] = make_node(
                                flowchart, model_data["Names"][v], "doubleoctagon"
                            )

                        else:
                            nodes[v] = make_node(
                                flowchart, model_data["Names"][v], "octagon"
                            )

                    elif v in model_data["U_YIELD_REACTOR"]:
                        nodes[v] = make_node(
                            flowchart, model_data["Names"][v], "octagon"
                        )

                    elif v in model_data["U_PP"]:
                        nodes[v] = make_node(flowchart, model_data["Names"][v], "house")

                    elif v in model_data["U_DIST"]:
                        nodes[v] = make_node(
                            flowchart, model_data["Names"][v], "circle"
                        )

                    else:
                        nodes[v] = make_node(flowchart, model_data["Names"][v], "box")

        for i, j in data.items():
            edges[i[0], i[1]] = make_link(
                flowchart, nodes[i[0]], nodes[i[1]], f"{j} t/h"
            )

        if not os.path.exists(path):
            os.makedirs(path)

        path = path + "/flowchart.png"

        flowchart.write_png(path)
