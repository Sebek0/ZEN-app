import React from "react";
import { BUNGIE_URL } from "../../../const/BungieUrl";
import Stat from "./Stat";
const GuardianStats = ({ guardian }) => {
	let stats = Object.entries(guardian.stats);
	stats = stats.filter((stat) => stat[0] !== "Power");

	return (
		<div className='flex flex-row h-3/12 rounded-t-xl p-3'>
			<img
				src={BUNGIE_URL + guardian.subclass.icon}
				alt='Zen'
				width={75}
				height={75}
				className='my-auto rounded-lg'></img>
			<div className='text-white text-xs flex flex-wrap ml-5'>
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
