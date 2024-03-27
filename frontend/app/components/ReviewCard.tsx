import { useEffect, useState } from 'react';
import { Review } from '../review.types';
import { generateStars } from '../utils/generateStars';
import { transformTimestamp } from '../utils/tranformUTCTimestamp';
import axios from 'axios';
import { Movie } from '../movie.types';
import Image from 'next/image';

interface Props {
  review: Review;
}

const ReviewCard = ({ review }: Props) => {
  // TODO: Need to get media info (title, image, etc.) in review
  const [movieData, setMovieData] = useState<Movie>();
  useEffect(() => {
    axios.get(`http://localhost:8000/movie/${review.MediaId}`).then(res => {
      setMovieData(res.data);
    });
  }, [review]);
  return (
    <>
      <div className="border-grey rounded-sm border">
        <Image
          src={`https://image.tmdb.org/t/p/original${movieData?.poster_path}`}
          width={200}
          height={300}
          alt={`${movieData?.title} poster`}
          className="rounded-t-sm"
        />
        <div className="flex rounded-b-sm bg-slate-300 p-1">
          <Image
            src={review.ProfilePictureUrl}
            height={20}
            width={20}
            alt="profile"
            className="mr-1 self-center rounded-full border border-slate-500"
          />
          <p className="font-semibold">{review.DisplayName || 'Anonymous'}</p>
        </div>
      </div>
      <div className="flex justify-between">
        <div className="flex">{generateStars(review.stars)}</div>
        <div>
          <p>{transformTimestamp(review.Date)}</p>
        </div>
      </div>
    </>
  );
};
export default ReviewCard;
