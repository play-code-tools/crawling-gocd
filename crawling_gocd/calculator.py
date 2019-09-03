
class Calculator:
    def __init__(self, strategyHandlers):
        self.strategyHandlers = strategyHandlers

    def work(self, pipelines):
        for handler in self.strategyHandlers:
            handler.work(pipelines)


