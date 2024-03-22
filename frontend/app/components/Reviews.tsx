import { StarIcon } from '@heroicons/react/20/solid';
import { cn } from '@/lib/utils';
import Image from 'next/image';
import { useEffect, useState } from 'react';
import { Review } from '@/app/review.types';

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
      fetch(`http://localhost:8000/reviews/${params.movieId}`)
        .then(res => res.json())
        .then(data => setReviews(data));
    }
  }, [params.movieId]);

  return (
    <div className="bg-white">
      <div>
        <h2 className="sr-only">Customer Reviews</h2>
        <div className="my-10">
          {reviews.map((review, reviewIdx) => (
            <div
              key={review.id}
              className="flex space-x-4 text-sm text-gray-500"
            >
              <div className="flex-none py-10">
                <Image
                  src="https://images.unsplash.com/photo-1551963831-b3b1ca40c98e"
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
                  {[0, 1, 2, 3, 4].map(rating => (
                    <div key={rating} className="relative">
                      <StarIcon
                        className={cn(
                          review.stars > rating
                            ? 'text-yellow-400'
                            : 'text-gray-300',
                          'h-5 w-5 flex-shrink-0'
                        )}
                        aria-hidden="true"
                      />
                      {review.stars > rating && review.stars < rating + 1 && (
                        <StarIcon
                          className="absolute left-0 top-0 h-5 w-5 flex-shrink-0"
                          style={{
                            // This style is to clip the star to display only a percentage of it
                            clipPath: 'inset(0 0 0 50%)',
                            // This is the RGB color equivalent of text-gray-300
                            color: 'rgb(209 213 219)'
                          }}
                          aria-hidden="true"
                        />
                      )}
                    </div>
                  ))}
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
    </div>
  );
}
