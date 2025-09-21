"""
    # 1. Obtener todos los offsets donde hay cambios de nota en cualquier voz
    all_offsets = set()
    for part in parts:
        for n in part.flat.notes:
            all_offsets.add(n.offset)
    all_offsets = sorted(all_offsets)

    # 2. Recorrer los pares de voces
    for indice1, indice2 in combinations(range(len(parts)), 2):
        voice1 = parts[indice1]
        voice2 = parts[indice2]

        # Convierte a stream para eficiencia y compatibilidad
        v1_notes = voice1.flatten().notes.stream()
        v2_notes = voice2.flatten().notes.stream()

        print(f"Beat Strengths de la voz {indice1+1}:")
        for n in voice1.recurse().notes:
            print(n, n.beatStrength)

        print(f"Beat Strengths de la voz {indice2+1}:")
        for n in voice2.recurse().notes:
            print(n, n.beatStrength)

        print(f"\nEstamos analizando las voces: {indice1+1} y {indice2+1}\n")

        for i in range(len(all_offsets) - 1):
            t0 = all_offsets[i]
            t1 = all_offsets[i+1]

            v1n1 = v1_notes.getElementAtOrBefore(t0)
            v1n2 = v1_notes.getElementAtOrBefore(t1)
            v2n1 = v2_notes.getElementAtOrBefore(t0)
            v2n2 = v2_notes.getElementAtOrBefore(t1)


            if v1n1 and v1n2 and v2n1 and v2n2:
                nota1 = v1n1.pitch.nameWithOctave
                nota2 = v1n2.pitch.nameWithOctave
                nota3 = v2n1.pitch.nameWithOctave
                nota4 = v2n2.pitch.nameWithOctave

                if case_1(nota1, nota2, nota3, nota4):
                    total_caso1 += 1
                if case_2(nota1, nota2, nota3, nota4):
                    total_caso2 += 1
                if case_3(nota1, nota2, nota3, nota4):
                    total_caso3 += 1

                vlq = voiceLeading.VoiceLeadingQuartet(v1n1, v1n2, v2n1, v2n2)
                vlqs.append(vlq)

    for i, vlq in enumerate(vlqs[:9]):
        print(f"\n--- VoiceLeadingQuartet {i+1} ---")
        print(f"v1n1 (nota superior inicial): {vlq.v1n1.nameWithOctave}")
        print(f"v1n2 (nota superior final): {vlq.v1n2.nameWithOctave}")
        print(f"v2n1 (nota inferior inicial): {vlq.v2n1.nameWithOctave}")
        print(f"v2n2 (nota inferior final): {vlq.v2n2.nameWithOctave}")
        print("Contrary motion: ", vlq.inwardContraryMotion())
    """