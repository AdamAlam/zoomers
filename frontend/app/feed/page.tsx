interface Props {}
const Feed = (props: Props) => {
  return (
    <div className="container flex flex-col justify-center">
      <div
        id="welcome-back"
        className="mb-4 border-2 border-red-700 text-center"
      >
        <h3 className="scroll-m-20 text-4xl font-bold tracking-tight lg:text-2xl">
          Wecome back {'<USERNAME HERE>'}. Heres what your friends have been
          watching.
        </h3>
      </div>

      <div id="new-from-friends">
        <h4 className="text-3xl font-bold tracking-tight lg:text-sm">
          New from Friends
        </h4>
        <div className="grid grid-cols-5">
          <div className="border-2 border-red-700">
            <img src="https://via.placeholder.com/150" alt="movie" />
            {/* Review author at bottom of image */}
            {/* Number of stars on bottom left */}
            {/* Date on bottom right */}
            {/* See: https://share.cleanshot.com/ggRHHqNf */}
          </div>
          <div className="border-2 border-red-700">Movie 2</div>
          <div className="border-2 border-red-700">Movie 3</div>
          <div className="border-2 border-red-700">Movie 4</div>
          <div className="border-2 border-red-700">Movie 5</div>
        </div>
      </div>
    </div>
  );
};
export default Feed;
