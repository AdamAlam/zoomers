import { Review } from '@/app/review.types';
import { cn } from '@/lib/utils';
import Image from 'next/image';
import { useEffect, useState } from 'react';
import { generateStars } from '../utils/generateStars';

export default function Reviews({ params }: { params: { movieId: string } }) {
  const [reviews, setReviews] = useState<Review[]>([]);

  useEffect(() => {
    const fetchReviews = async () => {
      const response = await fetch('/api/reviews');
      const data = await response.json();
      setReviews(data);
    };
    fetchReviews();
  }, []);

  // Get reviews for movie id
  useEffect(() => {
    if (params.movieId !== undefined) {
      fetch(`/api/reviews/${params.movieId}`)
        .then(res => res.json())
        .then(data => setReviews(data));
    }
  }, [params.movieId]);

  return (
    <div>
      <h2 className="sr-only">User Reviews</h2>
      <div className="my-10">
        {Array.isArray(reviews) &&
          reviews.map((review, reviewIdx) => (
            <div
              key={review.id}
              className="flex space-x-4 text-sm text-gray-500"
            >
              <div className="flex-none py-10">
                <Image
                  src={
                    review.ProfilePictureUrl ||
                    'https://images.unsplash.com/photo-1551963831-b3b1ca40c98e'
                  }
                  alt="reviewer avatar"
                  className="h-10 w-10 rounded-full bg-gray-100"
                  width={40}
                  height={40}
                />
              </div>
              <div
                className={cn(
                  reviewIdx === 0 ? '' : 'border-t border-gray-200',
                  'flex-1 py-10'
                )}
              >
                <h3 className="font-medium text-gray-900">
                  {review.DisplayName}
                </h3>
                <p>
                  <time dateTime={review.Date}>
                    {new Date(review.Date).toLocaleDateString('en-US', {
                      year: 'numeric',
                      month: 'long',
                      day: 'numeric',
                      hour: 'numeric',
                      minute: 'numeric',
                      timeZoneName: 'short'
                    })}
                  </time>
                </p>
                <div className="mt-4 flex items-center">
                  {generateStars(review.stars)}
                </div>
                {/* For screen reader */}
                <p className="sr-only">{review.stars} out of 5 stars</p>
                <div className="prose prose-sm mt-4 max-w-none text-gray-500">
                  {review.ReviewText}
                </div>
              </div>
            </div>
          ))}
      </div>
    </div>
  );
}
