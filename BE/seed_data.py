import pandas as pd

import sys
sys.path.append('../DogMatch')
from BE.database import get_foreign_key_id, row_exists
from BE.animal import Animal, DictCoatLength, DictCoatType, DictDogBreed, DogBreed


def seedDataDictBreeds(session, data_path) -> None:
    data = pd.read_csv(data_path)
    code_to_breed = {code: breed for code, breed in enumerate(data["Breed"].unique())}

    breeds = [DictDogBreed(key, value) for key, value in code_to_breed.items()]

    for breed in breeds:
        if not row_exists(session, "token", breed.token, DictDogBreed):
            session.add(breed)
    session.commit()


def seedDataDictCoatLength(session, data_path) -> None:
    data = pd.read_csv(data_path)
    code_to_coat_length = {
        code: coat_length
        for code, coat_length in enumerate(data["Coat Length"].unique())
    }

    coat_lengths = [
        DictCoatLength(key, value) for key, value in code_to_coat_length.items()
    ]

    for coat_length in coat_lengths:
        if not row_exists(session, "token", coat_length.token, DictCoatLength):
            session.add(coat_length)
    session.commit()


def seedDataDictCoatType(session, data_path) -> None:
    data = pd.read_csv(data_path)
    code_to_coat_type = {
        code: coat_type for code, coat_type in enumerate(data["Coat Type"].unique())
    }

    coat_types = [DictCoatType(key, value) for key, value in code_to_coat_type.items()]

    for coat_type in coat_types:
        if not row_exists(session, "token", coat_type.token, DictCoatType):
            session.add(coat_type)
    session.commit()


def seedDataDogBreed(session, data_path) -> None:
    data = pd.read_csv(data_path)

    for _, row in data.iterrows():
        dict_breed_id = get_foreign_key_id(session, DictDogBreed, row["Breed"])
        coat_type_id = get_foreign_key_id(session, DictCoatType, row["Coat Type"])
        coat_length_id = get_foreign_key_id(session, DictCoatLength, row["Coat Length"])

        dog_breed = DogBreed(
            dict_breed_id=dict_breed_id,
            affectionate_with_family=row["Affectionate With Family"],
            good_with_young_children=row["Good With Young Children"],
            good_with_other_dogs=row["Good With Other Dogs"],
            shedding_level=row["Shedding Level"],
            coat_grooming_frequency=row["Coat Grooming Frequency"],
            drooling_level=row["Drooling Level"],
            coat_type=coat_type_id,
            coat_length=coat_length_id,
            openness_to_strangers=row["Openness To Strangers"],
            playfulness_level=row["Playfulness Level"],
            watchdog_protective_nature=row["Watchdog/Protective Nature"],
            adaptability_level=row["Adaptability Level"],
            trainability_level=row["Trainability Level"],
            energy_level=row["Energy Level"],
            barking_level=row["Barking Level"],
            mental_stimulation_needs=row["Mental Stimulation Needs"],
        )

        if session.query(DogBreed).first() is None:
            session.add(dog_breed)
    session.commit()


def seedData(session, data_path) -> None:
    seedDataDictCoatType(session, data_path)
    seedDataDictCoatLength(session, data_path)
    seedDataDictBreeds(session, data_path)
    seedDataDogBreed(session, data_path)
