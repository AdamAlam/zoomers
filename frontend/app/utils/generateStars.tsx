import { StarIcon } from '@heroicons/react/20/solid';

export const generateStars = (rating: number) => {
  const stars = [];
  for (let i = 0; i < 5; i++) {
    if (rating > i) {
      if (rating < i + 1) {
        // Half star
        stars.push(<HalfStarIcon key={i} />);
      } else {
        // Full star
        stars.push(
          <StarIcon
            key={i}
            className="h-5 w-5 flex-shrink-0 text-yellow-400"
            aria-hidden="true"
          />
        );
      }
    } else {
      // Empty star
      stars.push(
        <StarIcon
          key={i}
          className="h-5 w-5 flex-shrink-0 text-gray-300"
          aria-hidden="true"
        />
      );
    }
  }
  return stars;
};

const HalfStarIcon = () => (
  <div className="relative h-5 w-5 flex-shrink-0">
    <StarIcon
      className="absolute left-0 top-0 h-5 w-5 text-yellow-400"
      aria-hidden="true"
    />
    <div style={{ clipPath: 'inset(0 0 0 50%)' }}>
      <StarIcon className="h-5 w-5 text-gray-300" aria-hidden="true" />
    </div>
  </div>
);
