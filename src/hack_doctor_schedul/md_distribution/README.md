### Алгоритм распределения нагрузки на основе предсказаний количества исследований
Классы и основные функции алгоритма находятся в библиотеке hack_doctor_schedul, в файле \src\hack_doctor_schedul\md_distribution\md_distribution.py.

Пример использования данного алгоритма находится в файле \scripts\md_distribution_example.py

На вход алгоритм принимает недельные предсказания количества исследований в виде pd.DataFrame, нормативы по видам исследований в формате списка словарей с указанием названия исследования (как в датафрейме с предсказаниями), количество условных единиц (у.е.) и тип медицинского работника, который описывает данное исследование, суммарное количество у.е. на одного врача, а также доля загрузки на одного врача с учетом погрешности модели (в данном случае, указываем 0,8 с расчетом на то, что в случае обычного прогноза врач будет работать с нагрузкой 0,8 с запасом в 20% на случай ошибок в прогннозе модели или срочных исследований).

Загрузку данных о врачах осуществляет класс объектов MDLoader с методами load_mds и get_mds. В данном случае для примера используется mock-реализация данного класса MockMDLoader: данный mock-объект генерирует количество врачей, необходимое для того, чтобы закрыть потребность во всех исследованиях.

MDPool - класс объектов для планирования расписания. Вызов метода create_md_scedule инициализированного объекта возвращает датафрейм с указанием количества исследований разных видов для каждого конкретного врача в течение периода времени (в данном случае - всех прогнозов по неделям, но алгоритм можно использовать и для другой дискретности). В каждой итерации учитывается как нагрузка врача на текущей неделе, так и суммарная накопленная натекущий момент в у.е. Данный объект инициализируется вместе со стратегией оптимизации расписания.

В данном случае используется жадный подход для распределения нагрузки по врачам. Для каждого врача с приоритетом врачей с минимальной суммарной нагрузкой распределяются исследования, соответствующие профилю врача. Исследования распределяются с приоритетом с максимальным количеством трудозатрат. Для каждого исследования этот цикл распределения нагрузки повторяется, пока все исследования не будут распределены по врачам. В данном случае использован наивный подход к составлению расписания, однако его в последствии возможно будет заменить на более сложный.