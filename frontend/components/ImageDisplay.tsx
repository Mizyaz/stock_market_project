// frontend/app/components/ImageDisplay.tsx

import { FC } from 'react'
import Image from 'next/image'

interface ImageDisplayProps {
  src: string
  alt: string
  width: number
  height: number
  title: string
}

const ImageDisplay: FC<ImageDisplayProps> = ({ src, alt, width, height, title }) => {
  return (
    <div className="mb-4">
      <h3 className="text-lg font-semibold mb-2">{title}</h3>
      <Image
        src={src}
        alt={alt}
        width={width}
        height={height}
        layout="responsive"
        className="rounded shadow"
      />
    </div>
  )
}

export default ImageDisplay