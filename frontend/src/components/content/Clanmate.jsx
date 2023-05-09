import PropTypes from "prop-types";
import React from "react";
import Guardian from "./Guardian";
const Clanmate = ({ clanmate }) => {
	return (
		<div className='mx-auto p-5 h-full w-full flex flex-col'>
			<div className="mx-auto">
				<span className='bg-secondary text-white rounded-xl text-center p-3 text-4xl w-auto'>
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

			{/* <div>
				<img
					src={BUNGIE_URL + clanmate.characters[0].emblem_path}
					alt='Zen'
					width={50}
					height={50}
					className='mx-auto my-auto rounded-lg'></img>
				<div className='text-white text-lg w-9/12'>
					<p>{clanmate.name}</p>
					<strong className='text-xs text-purple-600 drop-shadow-lg tracking-tighter'>
						{clanmate.characters[0].title}
					</strong>
				</div>
			</div> */}
		</div>
	);
};

Clanmate.propTypes = {
	clanmate: PropTypes.object.isRequired,
};

export default Clanmate;
