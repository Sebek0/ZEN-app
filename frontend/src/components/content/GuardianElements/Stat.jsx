import React from "react";
import { BUNGIE_URL } from "../../../const/BungieUrl";

const Stat = ({ stat }) => {
	const width = `${stat[1].value}%`;
	return (
		<div
			className='flex flex-row w-4/12 m-0 p-0 mx-3 my-1'
			title={stat[0]}>
			<img
				src={BUNGIE_URL + stat[1].icon}
				alt='Zen'
				width={30}
				height={30}
				className='ms-0 my-auto rounded-lg'
			/>
			<div className='flex flex-col w-8/12 ms-1 '>
				<span className='text-white text-md'>{stat[1].value}</span>
				<div className=' w-full bg-primary'>
					<div
						className='h-2 bg-neutral-500'
						style={{ width }}></div>
				</div>
			</div>
		</div>
	);
};

export default Stat;
