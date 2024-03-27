import { Review } from '../review.types';
import { generateStars } from '../utils/generateStars';
import { transformTimestamp } from '../utils/tranformUTCTimestamp';

interface Props {
  review: Review;
}

const ReviewCard = ({ review }: Props) => {
  // TODO: Need to get media info (title, image, etc.) in review
  return (
    <div>
      <div className="mt-4 flex items-center">
        {generateStars(review.stars)}
      </div>
      <p>{review.ReviewText}</p>
      <p>{transformTimestamp(review.Date)}</p>
    </div>
  );
};
export default ReviewCard;
