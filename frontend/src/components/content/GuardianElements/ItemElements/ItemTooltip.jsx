/* eslint-disable react/jsx-key */
import React from "react";
import Perk from "./Perk.jsx";
const ItemTooltip = ({ item, hovered }) => {
	return (
		<div
			className={`${
				hovered ? "rollDown duration-500 ease-in-out-cubic forwards" : "opacity-0 hidden"
			}  h-5/12 relative`}>
			<div className='absolute top-0 start-0 w-full h-full bg-white rounded-xl'>
				<div className='flex flex-col rounded-b-lg bg-gradient-to-b from-secondary to-primary shadow-xl'>
					<div className='flex flex-row justify-between'>
						<div className='flex flex-col space-y-5 m-5'>
							<span className='text-white text-lg text-bold'>
								Perks
							</span>
							{Object.entries(item[1].perks).map((perk) => {
								return (
									<div className='flex flex-row'>
										<Perk
											key={perk[1].name}
											size={30}
											perk={perk}></Perk>
										<span className='text-white text-xs ms-5'>{perk[1].name}</span>
									</div>
								);
							})}
						</div>
						<div className='flex flex-col space-y-5 m-5'>
							<span className='text-white text-lg text-bold'>
								Stats
							</span>
							{Object.entries(item[1].stats).map((stat) => {
								return (
									<div className='flex flex-row justify-between'>
										<span className='text-white text-xs me-5'>{stat[0]}</span>
										<span className='text-white text-xs font-bold'>{stat[1].value}</span>
									</div>
								);
							})}
						</div>
					</div>
				</div>
			</div>
		</div>
	);
};

export default ItemTooltip;
