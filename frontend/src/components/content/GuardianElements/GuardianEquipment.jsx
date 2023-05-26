import React from "react";
import { BUNGIE_URL } from "../../../const/BungieUrl.js";
import { ARMOR_SLOTS, WEAPON_SLOTS } from "../../../const/Items.js";
const GuardianEquipment = ({ guardian }) => {
	let items = Object.entries(guardian.items);
	const weapons = items.filter((item) => WEAPON_SLOTS.includes(item[0]));
	const armor = items.filter((item) => ARMOR_SLOTS.includes(item[0]));

	return (
		<div className='flex flex-row justify-around m-5'>
			<div className='flex flex-col'>
				{weapons.map((weapon) => (
					<div
						key={weapon[0]}
						className='m-3 cursor-pointer'>
						<div className='relative w-10'>
							<img
								src={BUNGIE_URL + weapon[1].common_data.item_icon}
								alt='Zen'
								height={10}
								className='mx-auto my-auto rounded-lg'></img>
							<img
								src={BUNGIE_URL + weapon[1].common_data.item_watermark}
								alt='Zen'
								className='absolute top-0 start-0'></img>
						</div>
					</div>
				))}
			</div>
			<div className='flex flex-col'>
				{armor.map((armor) => (
					<div
						key={armor[0]}
						className='m-3 cursor-pointer'>
						<div className='relative w-10'>
							<img
								src={BUNGIE_URL + armor[1].common_data.item_icon}
								alt='Zen'
								className='mx-auto my-auto rounded-lg'></img>
							<img
								src={BUNGIE_URL + armor[1].common_data.item_watermark}
								alt='Zen'
								height={10}
								className='absolute top-0 start-0'></img>
						</div>
					</div>
				))}
			</div>
		</div>
	);
};

export default GuardianEquipment;
