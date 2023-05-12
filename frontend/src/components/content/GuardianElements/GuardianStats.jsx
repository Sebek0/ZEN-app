import React from "react";
import { BUNGIE_URL } from "../../../const/BungieUrl";
import Stat from "./Stat";
const GuardianStats = ({ guardian }) => {
	let stats = Object.entries(guardian.stats);
	stats = stats.filter((stat) => stat[0] !== "Power");

	return (
		<div className='flex flex-row w-full h-3/12 rounded-t-xl p-5'>
			<img
				src={BUNGIE_URL + guardian.subclass.icon}
				alt='Zen'
				width={75}
				height={75}
				className='ms-0 my-auto rounded-lg'></img>
			<div className='text-white text-lg flex flex-wrap w-full ml-3'>
				{stats.map((stat) => (
					<Stat
						stat={stat}
						key={stat[0]}></Stat>
				))}
			</div>
		</div>
	);
};

export default GuardianStats;
