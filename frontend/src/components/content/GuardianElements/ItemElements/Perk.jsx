import React from "react";
import { BUNGIE_URL } from "../../../../const/BungieUrl.js";
const Perk = ({ perk }) => {
	return (
		<div
			key={perk[1].name}
			className='bg-slate-800 rounded-xl'
			title={perk[1].name}>
			<img
				src={BUNGIE_URL + perk[1].icon}
				alt='Zen'
				width={25}
				height={25}></img>
		</div>
	);
};

export default Perk;
