from src.structures import FilmId, VertexDto

f1 = FilmId(name="Брат 2", url="url1")
f2 = FilmId(name="57 секунд", url="url2")
f3 = FilmId(name="KK", url="url3")
vertexes = {
    f1: VertexDto(val=f1, source="s1", similar=[f3]),
    f2: VertexDto(val=f1, source="s1", similar=[f3]),
    f3: VertexDto(val=f1, source="s1", similar=[f3]),
}
