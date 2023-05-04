import React from "react";
import Zen from "../../assets/zen.gif";
import Clanmate from "../nav/Clanmate";
import PropTypes from "prop-types";


const Main = ({ displayedClanmateId }) => {
	return (
		<div className='flex flex-row w-full'>
			{displayedClanmateId === 0 ? (
				<p className='text-9xl mx-auto my-5'>
					<img
						src={Zen}
						alt='Zen'
						width={250}
						className='mx-auto my-auto rounded-lg'
					/>
				</p>
			) : (
				<Clanmate id={displayedClanmateId} />
			)}
		</div>
	);
};

Main.propTypes = {
	displayedClanmateId: PropTypes.number.isRequired,
};

export default Main;
