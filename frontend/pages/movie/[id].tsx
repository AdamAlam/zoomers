'use client';

import { useRouter } from 'next/router';

const MovieDetail = () => {
  const router = useRouter();
  const { id: movieId } = router.query;

  return <div className="flex px-3">{movieId}</div>;
};
export default MovieDetail;
