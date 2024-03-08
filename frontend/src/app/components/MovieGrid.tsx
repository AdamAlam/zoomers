"use client"
import Image from "next/image"
import { Movie } from "../movie.types"

interface Props {
  movies: Movie[]
}
const MovieGrid = ({movies}: Props) => {
  const imageBaseUrl = "https://image.tmdb.org/t/p/original";

  return (
    <div className="ml-5">
      <h1>Popular</h1>
      <div className="flex overflow-y-hidden overflow-x-scroll p-5">
        {movies.map((movie: Movie) => (
          <Image key={movie.id} src={`${imageBaseUrl}${movie.poster_path}`} className="object-contain mr-2" width={200} height={300}/>
        ))}
      </div>
    </div>
  )
}
export default MovieGrid