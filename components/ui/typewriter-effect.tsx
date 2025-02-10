"use client"

import { cn } from "@/lib/utils"
import { motion, AnimatePresence } from "framer-motion"
import { useEffect, useState } from "react"

export const TypewriterEffect = ({
    words,
    className,
    cursorClassName,
}: {
    words: {
        text: string
        className?: string
    }[]
    className?: string
    cursorClassName?: string
}) => {
    const [complete, setComplete] = useState(false)
    const [showCursor, setShowCursor] = useState(true)

    useEffect(() => {
        // First timeout for completing the typing effect
        const completeTimeout = setTimeout(() => {
            setComplete(true)
        }, 4000)

        // Second timeout for hiding the cursor after typing is complete
        const cursorTimeout = setTimeout(() => {
            setShowCursor(false)
        }, 4500) // 500ms after the typing completes

        return () => {
            clearTimeout(completeTimeout)
            clearTimeout(cursorTimeout)
        }
    }, [])

    const containerVariants = {
        hidden: { opacity: 0 },
        visible: {
            opacity: 1,
            transition: {
                staggerChildren: 0.3,
                delayChildren: 0.6,
            },
        },
    }

    const childVariants = {
        hidden: { opacity: 0, y: 20 },
        visible: {
            opacity: 1,
            y: 0,
            transition: {
                type: "spring",
                damping: 16,
                stiffness: 80,
                duration: 0.8,
            },
        },
    }

    return (
        <motion.div
            initial="hidden"
            animate="visible"
            variants={containerVariants}
            className={cn("text-4xl font-bold tracking-tighter sm:text-5xl md:text-6xl lg:text-7xl/none", className)}
        >
            <div className="inline-block">
                {words.map((word, idx) => {
                    return (
                        <motion.span
                            key={word.text + idx}
                            variants={childVariants}
                            className={cn("inline-block", word.className)}
                        >
                            {word.text}&nbsp;
                        </motion.span>
                    )
                })}
            </div>
            <AnimatePresence mode="wait">
                {showCursor && (
                    <motion.span
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0, transition: { duration: 0.3 } }}
                        transition={{
                            duration: 0.5,
                            repeat: showCursor ? Infinity : 0,
                            repeatType: "reverse",
                        }}
                        className={cn("inline-block h-[1em] w-[2px] bg-white ml-1", cursorClassName)}
                    />
                )}
            </AnimatePresence>
        </motion.div>
    )
} 