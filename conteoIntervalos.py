"""
1. Se realiza el conteo de intervalos haciendo uso de Voice Leading Quartets
"""

from music21 import *
from music21.interval import Interval
from music21 import converter, voiceLeading
from itertools import combinations

def inicializar():
    environment.set('musescoreDirectPNGPath', r"C:\Program Files\MuseScore 4\bin\MuseScore4.exe")
    environment.set('musicxmlPath', r"C:\Program Files\MuseScore 4\bin\MuseScore4.exe")
    environment.UserSettings()['musescoreDirectPNGPath']

def case_1(nota1,nota2, nota3, nota4):
    p1v1 = pitch.Pitch(nota1)
    p2v1 = pitch.Pitch(nota2)
    p1v2 = pitch.Pitch(nota3)
    p2v2 = pitch.Pitch(nota4)

    vert_int1 = interval.Interval(p1v1, p1v2)
    vert_int2 = interval.Interval(p2v1, p2v2)

    if ((vert_int1.semitones in [8, 9]) and (vert_int2.semitones in [12])):
        print(f"Evaluando: {p1v1.nameWithOctave} -> {p1v2.nameWithOctave} | {p2v1.nameWithOctave} -> {p2v2.nameWithOctave}")
        print(f"Intervalos: {vert_int1.semitones} (v1) - {vert_int2.semitones} (v2)\n")
        return True
    else:
        return False

def case_2(nota1,nota2, nota3, nota4):
    p1v1 = pitch.Pitch(nota1)
    p2v1 = pitch.Pitch(nota2)
    p1v2 = pitch.Pitch(nota3)
    p2v2 = pitch.Pitch(nota4)

    vert_int1 = interval.Interval(p1v1, p1v2)
    vert_int2 = interval.Interval(p2v1, p2v2)

    if (vert_int1.semitones == 4 and vert_int2.semitones == 7):
        print(f"Evaluando: {p1v1.nameWithOctave} -> {p1v2.nameWithOctave} | {p2v1.nameWithOctave} -> {p2v2.nameWithOctave}")
        print(f"Intervalos: {vert_int1.semitones} (v1) - {vert_int2.semitones} (v2)\n")
        return True
    else:
        return False

def case_3(nota1,nota2, nota3, nota4):
    p1v1 = pitch.Pitch(nota1)
    p2v1 = pitch.Pitch(nota2)
    p1v2 = pitch.Pitch(nota3)
    p2v2 = pitch.Pitch(nota4)

    vert_int1 = interval.Interval(p1v1, p1v2)
    vert_int2 = interval.Interval(p2v1, p2v2)

    if (vert_int1.semitones == 3 and vert_int2.semitones == 0):

        print(f"Evaluando: {p1v1.nameWithOctave} -> {p1v2.nameWithOctave} | {p2v1.nameWithOctave} -> {p2v2.nameWithOctave}")
        print(f"Intervalos: {vert_int1.semitones} (v1) - {vert_int2.semitones} (v2)\n")

        return True
    else:
        return False

def voiceLeadingConteo(archivo):
    score = converter.parse(archivo)
    parts = score.parts

    print(f"Hay {len(parts)} voces y son las siguientes: {parts}")

    total_caso1 = 0
    notas_caso1 = []

    total_caso2 = 0
    notas_caso2 = []

    total_caso3 = 0
    notas_caso3 = []

    vlqs = []

    # Obtener todos los números de compás únicos presentes en la partitura
    compas_numeros = sorted(
        set(m.number for part in parts for m in part.getElementsByClass('Measure') if m.number is not None)
    )

    for compas_num in compas_numeros:
        print(f"\n--- Compás {compas_num} ---")
        compases = [part.measure(compas_num) for part in parts]

        for indice1, indice2 in combinations(range(len(compases)), 2):
            compas1 = compases[indice1]
            compas2 = compases[indice2]
            print(f"\nAnalizando voces {indice1+1} y {indice2+1} en el compás {compas_num}:\n")

            if compas1 is not None and compas2 is not None:
                v1_notes = compas1.flatten().notes.stream()
                v2_notes = compas2.flatten().notes.stream()

            n1_anterior = None
            n2_anterior = None

            for n1, n2 in zip(v1_notes, v2_notes):
                if n1.offset != n2.offset:
                    print(f"Offset entre {n1.nameWithOctave} y {n2.nameWithOctave}")
                    continue

                vert_int = interval.Interval(n2.pitch, n1.pitch) 
                
                if n1_anterior is not None and n2_anterior is not None:
                    vert_int2 = interval.Interval(n2_anterior.pitch, n1_anterior.pitch)

                    print(f"Vertical interval actual -> {vert_int.semitones} con Nota 1: {n1.nameWithOctave} y Nota 2: {n2.nameWithOctave}")
                    print(f"Vertical interval anterior -> {vert_int2.semitones} con Nota 1: {n1_anterior.nameWithOctave} y Nota 2: {n2_anterior.nameWithOctave}")

                #CASO 1
                if vert_int.semitones == 12 and n1.beatStrength == 1.0 and n2.beatStrength == 1.0 and n1.offset == n2.offset:
                    print(f"Posible intervalo de 12 semitonos entre {n1.nameWithOctave} y {n2.nameWithOctave} en el compás {compas_num}")
                    notas_caso1.append((n1.nameWithOctave, n2.nameWithOctave, "Compas " + str(compas_num)))
                    total_caso1 += 1

                #CASO 2
                if vert_int.semitones == 7 and n1.beatStrength == 1.0 and n2.beatStrength == 1.0 and n1.offset == n2.offset:
                    print(f"Posible intervalo de 7 semitonos entre {n1.nameWithOctave} y {n2.nameWithOctave} en el compás {compas_num}")
                    notas_caso2.append((n1.nameWithOctave, n2.nameWithOctave, "Compas " + str(compas_num)))
                    total_caso2 += 1

                #CASO 3
                if vert_int.semitones == 0 and n1.beatStrength == 1.0 and n2.beatStrength == 1.0 and n1.offset == n2.offset:
                    print(f"Posible intervalo de 0 semitonos entre {n1.nameWithOctave} y {n2.nameWithOctave} en el compás {compas_num}")
                    notas_caso3.append((n1.nameWithOctave, n2.nameWithOctave, "Compas " + str(compas_num)))
                    total_caso3 += 1

                n1_anterior = n1
                n2_anterior = n2

    print(f"\nTotal de casos 1 encontrados: {total_caso1}")
    print(f"Casos: ")
    for caso in notas_caso1:
        print(f"- {caso}")
    print(f"\nTotal de casos 2 encontrados: {total_caso2}")
    print(f"Casos: ")
    for caso in notas_caso2:
        print(f"- {caso}")
    print(f"\nTotal de casos 3 encontrados: {total_caso3}")
    print(f"Casos: ")
    for caso in notas_caso3:
        print(f"- {caso}")

    #score.show()
