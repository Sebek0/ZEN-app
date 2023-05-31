import React from "react";
import { BUNGIE_URL } from "../../../const/BungieUrl";
import Stat from "./Stat";
const GuardianStats = ({ guardian }) => {
	let stats = Object.entries(guardian.stats);
	stats = stats.filter((stat) => stat[0] !== "Power");

	return (
		<div className='flex flex-row h-3/12 p-3 bg-primary/50'>
			<img
				title={guardian.subclass.name}
				src={BUNGIE_URL + guardian.subclass.icon}
				alt='Zen'
				width={95}
				height={95}
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
