from Task.MLtask import PredictionTask, PredictionResult
from Users.user import User


class MLService:
    def __init__(self):
        pass

    def run_task(self, task: PredictionTask, user: User):
        task.start()
        cost = task.get_cost()

        if user.get_balance() < cost:
            task.fail("Недостаточно средств")
            return task

        output = task._model.predict(task._audio)
        result = PredictionResult(task._task_id, output, cost)
        user.decrease_balance(cost)
        task.complete(result)
        return task
