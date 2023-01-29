.PHONY: memory

memory:
	# malloc_one_gig
	gcc -O0 -I ./helpers/  memory/malloc_one_gig.c -o bins/memory/malloc_one_gig
	gcc -S -o asm/memory/malloc_one_gig.s memory/malloc_one_gig.c

	# allocate_small_segment
	gcc -O0 -I ./helpers/  memory/allocate_small_segment.c -o bins/memory/allocate_small_segment
	gcc -I ./helpers/  memory/allocate_small_segment.c -o bins/memory/allocate_small_segment_optimized
	
grep_memory:
	objdump -d bins/memory/allocate_small_segment_optimized | grep "brk" || echo "no match"
	objdump -d bins/memory/allocate_small_segment | grep "brk"  || echo "no match"
	