import React from "react";
import { BUNGIE_URL } from "../../../const/BungieUrl";

const Stat = ({ stat }) => {
	const icon = BUNGIE_URL + "/common/destiny2_content/icons/bbf5c71ea4bf181a9ed177031b6a26a4.jpg";

	// Calculate the width based on the stat value
	const width = `${stat[1]}%`;

	return (
		<div className='flex flex-row w-24 m-0 p-0'>
			<img
				src={icon}
				alt='Zen'
				width={25}
				height={25}
				className='ms-0 my-auto rounded-lg'
			/>
			<div className='flex flex-col w-5/12 mx-auto'>
				<span className='text-white text-xxs'>{stat[1]}</span>
				<div className='mb-6 h-2 w-full bg-primary'>
					<div
						className='h-2 bg-neutral-500'
						style={{ width }}></div>
				</div>
			</div>
		</div>
	);
};

export default Stat;
