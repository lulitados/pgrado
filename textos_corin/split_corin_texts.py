import io

with io.open('Corin.txt', 'r') as corin_source:
    new_corin_doc = None
    for line in corin_source:
        if line.startswith('*Texto: P'):
            # Start of new document
            if new_corin_doc is not None:
                new_corin_doc.close()
            new_corin_doc = io.open(
                "corin_sources/corin_{}.txt".format(line.strip('*Texto: ').lower().rstrip()),
                "w")

        new_corin_doc.write(line)

    new_corin_doc.close()
