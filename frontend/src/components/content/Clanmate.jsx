import PropTypes from "prop-types";
import React from "react";
import Guardian from "./Guardian";
const Clanmate = ({ clanmate }) => {
	return (
		<div className='mx-auto p-5 h-full w-full flex flex-col'>
			<div className='mx-auto'>
				<span className=' text-white rounded-xl text-center p-3 text-xl bg-secondary'>
					{clanmate.name}
				</span>
			</div>
			<div className='flex flex-col lg:flex-row w-full mx-auto'>
				{clanmate.characters.map((character) => (
					<Guardian
						guardian={character}
						key={character.character_id}></Guardian>
				))}
			</div>
		</div>
	);
};

Clanmate.propTypes = {
	clanmate: PropTypes.object.isRequired,
};

export default Clanmate;
