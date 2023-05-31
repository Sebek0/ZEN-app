/* eslint-disable react/prop-types */
import React from "react";
import { BUNGIE_URL } from "../../../../const/BungieUrl.js";
import Perk from "./Perk.jsx";
import ItemTooltip from "./ItemTooltip.jsx";

const Item = ({ item }) => {
	const [hovered, setHovered] = React.useState(false);

	return (
		<>
			<div
				className='flex flex-row z-10 '
				onMouseEnter={() => setHovered(true)}
				onMouseLeave={() => setHovered(false)}>
				<div
					key={item[0]}
					className='m-3 flex flex-row transform transition-transform duration-500 ease-in-out hover:scale-105 w-full'
					title={item[1].common_data.item_name}>
					<div className='relative w-20'>
						<img
							src={BUNGIE_URL + item[1].common_data.item_icon}
							alt='Zen'
							height={15}
							className='mx-auto my-auto rounded-lg'></img>
						{item[1].common_data.item_watermark !== null ? (
							<img
								src={BUNGIE_URL + item[1].common_data.item_watermark}
								alt='Zen'
								className='absolute top-0 start-0'></img>
						) : null}
					</div>
					<div className='flex flex-col'>
						<span className='text-white text-md ms-5'>
							{item[1].common_data.item_name} {item[1].perks[0]}
						</span>
						<div className='flex flex-row ms-5 space-x-3'>
							{Object.entries(item[1].perks)
								.slice(0, 6)
								.map((perk) => {
									return (
										<Perk
											size={25}
											key={perk[1].name}
											perk={perk}></Perk>
									);
								})}
							{Object.entries(item[1].perks).length > 6 && <span className='text-white'>...</span>}
						</div>
					</div>
				</div>
			</div>
			<ItemTooltip
				item={item}
				hovered={hovered}></ItemTooltip>
		</>
	);
};

export default Item;
