from src.structures import FilmId, Vertex


f1 = FilmId(name="F1", url="url1")
f2 = FilmId(name="F2", url="url2")
f3 = FilmId(name="F3", url="url3")
f4 = FilmId(name="F4", url="url4")
f5 = FilmId(name="F5", url="url5")
f6 = FilmId(name="F6", url="url6")


vertexes = [
    Vertex(val=f1, similar=[f2, f3]),
    Vertex(val=f2, similar=[f3, f4]),
    Vertex(val=f3, similar=[f2, f4]),
    Vertex(val=f4, similar=[f3, f5, f6]),
    Vertex(val=f5, similar=[]),
    Vertex(val=f6, similar=[f4]),
]
