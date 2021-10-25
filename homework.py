TRAINING_SWIMMING = 'SWM'
TRAINING_RUNNING = 'RUN'
TRAINING_SPORTSWALKING = 'WLK'


class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self, training_type: str,
                 duration: float, distance: float,
                 speed: float, calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:,.3f} ч.; '
                f'Дистанция: {self.distance:,.3f} км; '
                f'Ср. скорость: {self.speed:,.3f} км/ч; '
                f'Потрачено ккал: {self.calories:,.3f}.'
                )


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000
    TRAINING_NAME = 'Training'

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """
        Вернуть информационное сообщение
        о выполненной тренировке.
        """
        obj = InfoMessage(self.TRAINING_NAME,
                          self.duration,
                          self.get_distance(),
                          self.get_mean_speed(),
                          self.get_spent_calories()
                          )
        return obj


class Running(Training):
    """Тренировка: бег."""
    COEF_CALORIE_1 = 18
    COEF_CALORIE_2 = 20
    COEF_CALORIE_3 = 60
    TRAINING_NAME = 'Running'

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.distance = self.get_distance()
        self.speed = self.get_mean_speed()
        self.calories = self.get_spent_calories()

    def get_spent_calories(self) -> float:
        a = self.COEF_CALORIE_1 * self.speed - self.COEF_CALORIE_2
        b = self.duration * self.COEF_CALORIE_3
        return a * self.weight / self.M_IN_KM * b


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEF_CALORIE_1 = 0.035
    COEF_CALORIE_2 = 0.029
    COEF_CALORIE_3 = 60
    TRAINING_NAME = 'SportsWalking'

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height
        self.distance = self.get_distance()
        self.speed = self.get_mean_speed()
        self.calories = self.get_spent_calories()

    def get_spent_calories(self) -> float:
        a = self.COEF_CALORIE_1 * self.weight
        b = ((self.speed ** 2) // self.height)
        c = self.COEF_CALORIE_2 * self.weight
        d = self.duration * self.COEF_CALORIE_3
        return (a + b * c) * d


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    COEF_CALORIE_1 = 1.1
    COEF_CALORIE_2 = 2
    TRAINING_NAME = 'Swimming'

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool
        self.distance = self.get_distance()
        self.speed = self.get_mean_speed()
        self.calories = self.get_spent_calories()

    def get_mean_speed(self) -> float:
        a = self.length_pool * self.count_pool / self.M_IN_KM
        return a / self.duration

    def get_spent_calories(self) -> float:
        a = self.speed + self.COEF_CALORIE_1
        b = self.COEF_CALORIE_2 * self.weight
        return a * b


def read_package(workout_type: str,
                 data: list
                 ) -> Training:
    """Прочитать данные полученные от датчиков."""
    dict_train = {TRAINING_SWIMMING: Swimming,
                  TRAINING_RUNNING: Running,
                  TRAINING_SPORTSWALKING: SportsWalking
                  }
    return dict_train[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        (TRAINING_SWIMMING, [720, 1, 80, 25, 40]),
        (TRAINING_RUNNING, [15000, 1, 75]),
        (TRAINING_SPORTSWALKING, [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
