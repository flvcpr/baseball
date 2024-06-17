import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleCreaGrafo(self, e):
        if self._view._ddAnno.value is None:
            self._view._txt_result.controls.append(ft.Text("Seleziona un anno dal menu"))
            return
        self._model.buildGraph(self._view._ddAnno.value)
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text("Grafo creato"))
        n,a = self._model.getGraphDetails()
        self._view._txt_result.controls.append(ft.Text(f"Grafo costruito on {n} nodi e {a} archi"))
        self._view.update_page()

    def handleDettagli(self, e):
        vicini = self._model.getSortedNeighbors(self._selectedTeam)
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text(f"Stampo i vicini di {self._selectedTeam} con peso arco"))
        for v in vicini:
            self._view._txt_result.controls.append(ft.Text(f"{v[1]}-{v[0]}"))
        self._view.update_page()


    def handlePercorso(self, e):
        pass

    def handleDDYearSelection(self, e):
        teams = self._model.getTeamsOfYear(self._view._ddAnno.value)
        self._view._txtOutSquadre.controls.clear()
        self._view._txtOutSquadre.controls.append(
            ft.Text(f"Ho trovato {len(teams)} "
                    f"squade che hanno giocato nel {self._view._ddAnno.value}."))
        for t in teams:
            self._view._txtOutSquadre.controls.append(ft.Text(f"{t.teamCode}"))
            self._view._ddSquadra.options.append(
                ft.dropdown.Option(data=t,
                                   text=t.teamCode,
                                   on_click=self.readDDTeams)
            )
        self._view.update_page()

    def readDDTeams(self, e):
        if e.control.data is None:
            self._selectedTeam = None
        else:
            self._selectedTeam = e.control.data
        print(f"readDDTeams called -- {self._selectedTeam}")

    def fillDDYear(self):
        years = self._model.getYears()
        yearsDD = map(lambda x: ft.dropdown.Option(x), years)
        self._view._ddAnno.options = yearsDD
        self._view.update_page()

        # yearsDD = []
        # for y in years:
        #     yearsDD.append(ft.dropdown.Option(y))
